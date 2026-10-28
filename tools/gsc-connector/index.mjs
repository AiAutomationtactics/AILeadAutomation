#!/usr/bin/env node
// Google Search Console service-account connector. No third-party dependencies.
// Never place a private key in this file or GitHub repository.
import { createSign } from 'node:crypto';
const PROPERTY=process.env.GSC_PROPERTY||'https://leadgflow.vercel.app/';
const SITEMAP=process.env.GSC_SITEMAP||new URL('sitemap.xml',PROPERTY).href;
const AUTH='https://oauth2.googleapis.com/token';
const encoded=v=>Buffer.from(v).toString('base64url');
function credentials(){
  const secret=process.env.GSC_SERVICE_ACCOUNT_JSON_B64;
  if(!secret) return null;
  let c;
  try{c=JSON.parse(Buffer.from(secret,'base64').toString('utf8'));}
  catch{throw Error('The configured service-account secret is invalid JSON.');}
  if(c.type!=='service_account'||!c.client_email||!c.private_key)throw Error('A valid service-account credential is required.');
  if(c.token_uri&&c.token_uri!==AUTH)throw Error('Unexpected token endpoint.');
  return c;
}
async function tokenFor(c){
  const now=Math.floor(Date.now()/1000);
  const claim={iss:c.client_email,scope:'https://www.googleapis.com/auth/webmasters',aud:AUTH,iat:now,exp:now+3300};
  const header=encoded(JSON.stringify({alg:'RS256',typ:'JWT'}));
  const payload=encoded(JSON.stringify(claim));
  const value=header+'.'+payload;
  const signer=createSign('RSA-SHA256');signer.update(value);signer.end();
  const assertion=value+'.'+signer.sign(c.private_key,'base64url');
  const body=new URLSearchParams({grant_type:'urn:ietf:params:oauth:grant-type:jwt-bearer',assertion});
  const res=await fetch(AUTH,{method:'POST',headers:{'content-type':'application/x-www-form-urlencoded'},body,signal:AbortSignal.timeout(20000)});
  if(!res.ok)throw Error('Google token exchange failed (HTTP '+res.status+'). Check service account key and API enablement.');
  const data=await res.json();
  if(!data.access_token)throw Error('Google returned no access token.');
  return data.access_token;
}
async function request(token,path,method='GET',body){
  const headers={'Authorization':'Bearer '+token,'Accept':'application/json'};
  if(body!==undefined)headers['Content-Type']='application/json';
  const res=await fetch(path,{method,headers,body:body===undefined?undefined:JSON.stringify(body),signal:AbortSignal.timeout(30000)});
  if(!res.ok)throw Error('Search Console API returned HTTP '+res.status+' for '+method+'. Check property and permissions.');
  const raw=await res.text();
  return raw?JSON.parse(raw):{};
}
async function main(){
  const command=process.argv[2]||'audit';
  if(!['audit','inspect','submit-sitemap'].includes(command))throw Error('Unknown command. Use audit, inspect, or submit-sitemap.');
  const cred=credentials();
  if(!cred){console.log('SKIPPED: GitHub Actions secret GSC_SERVICE_ACCOUNT_JSON_B64 is not set. No Google connection is active.');return;}
  const token=await tokenFor(cred);
  const properties=await request(token,'https://www.googleapis.com/webmasters/v3/sites');
  const permission=(properties.siteEntry||[]).find(x=>x.siteUrl===PROPERTY);
  if(!permission||!['siteOwner','siteFullUser'].includes(permission.permissionLevel))throw Error('This service account does not have Full/Owner permission to '+PROPERTY);
  const siteUrl='https://www.googleapis.com/webmasters/v3/sites/'+encodeURIComponent(PROPERTY);
  if(command==='audit'){
    const d=await request(token,siteUrl+'/sitemaps');
    const entries=(d.sitemap||[]).map(s=>({path:s.path,status:s.isPending?'pending':'processed',errors:s.errors||0,warnings:s.warnings||0,lastSubmitted:s.lastSubmitted||null}));
    console.log(JSON.stringify({property:PROPERTY,permission:permission.permissionLevel,sitemaps:entries},null,2));return;
  }
  if(command==='inspect'){
    const url=process.env.GSC_INSPECT_URL||PROPERTY;
    if(!url.startsWith(PROPERTY)||!url.startsWith('https://'))throw Error('Inspected URL must be under this HTTPS URL-prefix property.');
    const d=await request(token,'https://searchconsole.googleapis.com/v1/urlInspection/index:inspect','POST',{siteUrl:PROPERTY,inspectionUrl:url,languageCode:'en-US'});
    const s=d.inspectionResult?.indexStatusResult||{};
    console.log(JSON.stringify({property:PROPERTY,inspected:url,verdict:s.verdict||null,coverageState:s.coverageState||null,robotsTxtState:s.robotsTxtState||null,indexingState:s.indexingState||null},null,2));return;
  }
  const p=new URL(PROPERTY),s=new URL(SITEMAP);
  if(p.origin!==s.origin||s.protocol!=='https:')throw Error('Sitemap must be HTTPS and hosted on the property origin.');
  await request(token,siteUrl+'/sitemaps/'+encodeURIComponent(SITEMAP),'PUT');
  console.log('Google accepted sitemap submission for '+SITEMAP+'. This does NOT guarantee indexing.');
}
main().catch(e=>{console.error('ERROR: '+e.message);process.exitCode=1;});
