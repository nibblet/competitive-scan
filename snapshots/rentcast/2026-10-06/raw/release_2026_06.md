---
agentTools:
  projectIndex: https://developers.rentcast.io/llms.txt
---

# New API Key Security Features

This API update added new API key security and restriction settings to help keep your API keys secure and reduce the risk of unauthorized access.

Check out the highlights below:

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## API Key Restrictions

* You can now configure IP restrictions for each API key by whitelisting specific IP addresses or IP address ranges that will be allowed to use each key. [Learn more](https://developers.rentcast.io/reference/security#ip-restrictions) about configuring IP restrictions
* You can also configure endpoint restrictions for each API key by selecting specific endpoints that each key will be allowed to access. [Learn more](https://developers.rentcast.io/reference/security#endpoint-restrictions) about configuring endpoint restrictions
* You can view and configure the new security restrictions for each API key from your <Anchor target="_blank" href="https://app.rentcast.io/app/api">API dashboard</Anchor>
* Visit the new [security](https://developers.rentcast.io/reference/security) page in our API docs to learn about security best practices, API key restrictions, request logging controls, and the security measures we take to protect our platform

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Property Valuation ([`/avm/value`](https://developers.rentcast.io/reference/value-estimate), [`/avm/rent/long-term`](https://developers.rentcast.io/reference/rent-estimate-long-term))

* We've increased the accuracy of our value and rent estimates by improving our comparable correlation algorithm and AVM methodology

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

Our [API documentation](https://developers.rentcast.io/reference) has been updated to reflect the above changes, and you can view it at any time to review our data sets and API endpoints in more detail.

If you have any questions about this update, or have additional feature requests or suggestions, contact us by launching the live chat at the bottom right of this website, or by sending an email to <support@rentcast.io>.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

<Callout icon="🚀" theme="okay">
  ### Getting Started

  To get started using our property data API, <Anchor target="_blank" href="https://app.rentcast.io/app/api">create a RentCast account</Anchor> to access your API dashboard and generate your first API key. [Read this guide](https://developers.rentcast.io/reference/getting-started-guide) for an in-depth walkthrough.
</Callout>

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>