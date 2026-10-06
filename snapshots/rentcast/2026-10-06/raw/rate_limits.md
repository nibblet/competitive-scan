---
updatedAt: 2026-08-13T19:41:58.000Z
agentTools:
  projectIndex: https://developers.rentcast.io/llms.txt
---

# Rate Limits

The RentCast API has a rate limit of 20 requests per second.

Our API has a hard limit of **20 requests per second**, per API key, regardless of your billing or subscription plan.

If you exceed this limit, you will receive an error with a `429` HTTP status code and the following body:

```json 429 Error Example
{
  "status": 429,
  "error": "auth/rate-limit-exceeded",
  "message": "The rate limit of 20 requests per second has been exceeded"
}
```

<br />

We recommend creating [separate API keys](https://developers.rentcast.io/reference/getting-started-guide#creating-an-api-key) for each of your applications, integrations or environments, and throttling your requests to stay within this rate limit.

If your application requires a higher sustained request rate, you can create multiple API keys for different applications, services or workloads. [Contact us](mailto:support@rentcast.io) if you need help planning a higher-volume integration.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>