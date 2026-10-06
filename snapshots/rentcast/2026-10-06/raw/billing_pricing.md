---
updatedAt: 2026-08-24T18:45:08.000Z
agentTools:
  projectIndex: https://developers.rentcast.io/llms.txt
---

# Billing and Pricing

Learn about our pricing and managing billing for your API subscription.

Our API has a transparent and predictable pricing model that scales with your API request volume and gives you access to nationwide property, rental and listing data at a competitive cost.

You can manage your API subscription and billing at any time from your <Anchor target="_blank" href="https://app.rentcast.io/app/api">API dashboard</Anchor> without the need to contact our support or sales teams.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## RentCast API Pricing

We offer several API pricing plans with different monthly API request limits to support different clients, integrations and use cases. They all give you access to the same nationwide data sets and endpoints.

Our API plans are billed monthly and do not come with any long-term contracts or commitments. You can start, change or stop your API plan at any time.

<Anchor target="_blank" href="https://www.rentcast.io/api#api-pricing">Visit our website</Anchor> to view our current API pricing information, or [contact us](mailto:support@rentcast.io) if you're interested in higher-volume enterprise plans.

We recommend starting with our **Developer** plan when developing and testing your integration, which includes 50 free API requests per month, with a small overage fee for additional requests beyond that limit.

<Callout icon="📘" theme="info">
  Our API billing plans have a fixed monthly price, as well as a per-request overage fee. Once you reach your monthly request limit, you will be charged the overage fee for each additional request.
</Callout>

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Managing Your API Subscription

An active API subscription is required to make requests to our API and to activate your API keys.

You can start, change or stop your API subscription at any time from your <Anchor target="_blank" href="https://app.rentcast.io/app/api">API dashboard</Anchor> page, by scrolling down to the **API Billing** section:

<Image src="https://files.readme.io/301a6d42c858838a7167e79aec1e6b4a214c2d57632eca15832bbd8710d458d1-rentcast-manage-api-subscription.png" alt="Managing a RentCast API subscription" align="center" />

<br />

When activating a new API subscription, your payment method will be charged for the first month of usage at that time, unless you've selected the free Developer plan.

You can switch to a different API plan at any time during your billing period. When you upgrade or downgrade your plan:

* Your billing date will reset to the current date
* Your monthly API request limit will reset to match your new plan
* Any accumulated overage fees from your current billing period will be charged to your payment method
* Our billing system will automatically apply a credit for any unused portion of your current billing period
* Your payment method will be charged for the new plan's monthly price, after applying that credit

Depending on the credit amount, the new plan's price, and any accumulated overage fees, your immediate charge may be lower than the new plan's regular monthly price, higher due to overage fees, or there may be no immediate charge at all.

When canceling an existing API subscription, your subscription will be set to cancel at the end of its current billing period, and you can continue making API requests until then. Any accumulated overage fees will be charged to your payment method at the end of the current billing period.

<Callout icon="⚠️" theme="warn">
  Your API request quota will reset at the end of each billing period, or when you switch to a different API plan. Any unused API requests **will not carry over** to the new billing period.
</Callout>

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Updating Your Payment Information

You can update your payment information from the <Anchor target="_blank" href="https://app.rentcast.io/app/account/billing">billing page</Anchor> in your account settings. The payment method you save will be used for both your RentCast API subscription and RentCast platform subscription, if you have one:

<Image src="https://files.readme.io/fac0af561957990e08ba4f23fbd33bbc556054174a689641008049b3a66ea4a9-rentcast-update-payment-method.png" alt="Updating RentCast API payment information" align="center" />

<Callout icon="⚠️" theme="warn">
  It is important to keep your payment information up to date. If any of your API subscription payments fail, your API access **will be suspended**, and all API requests made using your API keys will fail until the payment issue is resolved.
</Callout>

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Viewing Invoices and Receipts

You can view and download past invoices and receipts for your API subscription from the <Anchor target="_blank" href="https://app.rentcast.io/app/account/billing">billing page</Anchor> in your account settings:

<Image src="https://files.readme.io/79f8c87424a2430be49f2c83b1a84b859ed0910ac58ee2f6d7d73a5344bb6a9b-rentcast-payment-history.png" alt="Viewing RentCast API invoices and receipts" align="center" />

<br />

Each invoice and receipt will show the number of API requests made during the billing period, as well as any overage fees that were charged for requests over your current plan's API request limit.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Billing Error Codes

If you do not have an active subscription, or if there is a billing issue with your existing subscription, you will receive a 403 error code when making API requests:

```json 403 Error Example
{
  "status": 403,
  "error": "billing/subscription-inactive",
  "message": "The provided API key is not associated with an active API subscription. View subscription status on your API dashboard: https://app.rentcast.io/app/api"
}
```

Visit your <Anchor target="_blank" href="https://app.rentcast.io/app/api">API dashboard</Anchor> to view the status of your subscription and fix any billing issues to continue using our API and making requests.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Frequently Asked Questions

**Can I try your API for free?**

Yes, we offer a free Developer plan, which includes up to 50 API requests per month to any of our endpoints free of charge, and has a small overage fee for additional requests over 50.

This is the API plan we recommend you use when testing our API and developing your integration. [View this guide](https://developers.rentcast.io/reference/getting-started-guide) when you're ready to get started.

<br />

**What if I need more API requests for testing or development?**

If you need more than the 50 free API requests included with our Developer plan for testing, we recommend upgrading to one of our paid plans, or implementing <Anchor target="_blank" href="https://blog.postman.com/what-is-api-mocking">API request mocking</Anchor> in your integration to avoid making excessive live API requests.

You can also [contact us](mailto:support@rentcast.io), and we can add a credit to your account to facilitate additional API testing or development as a one-time courtesy.

<br />

**Do you bill based on how many requests I make, or how much data I retrieve?**

We only track the number of successful API requests you make for billing purposes. A "successful API request" is an HTTP request to any of our endpoints that returns a 200 status code and a response body.

It doesn't matter how much data you retrieve via each API request - it will only count as one request for billing purposes. You will also not be billed for requests that return an error (a status code other than 200).

<br />

**What happens when I exceed my API plan's monthly request limit?**

Each of our API plans has a set number of API requests included in the monthly price, as well as an overage fee that will be charged for additional requests.

If you exceed your monthly API request limit, you will be charged an overage fee for each additional request. If this happens regularly, we recommend upgrading to the next available API plan.

<br />

**Can I disable overages or set a hard usage cap on my API requests?**

We do not currently support hard usage caps or automatic API request blocking when you reach your current plan's monthly request limit.

If you require this functionality, we recommend implementing usage monitoring and API request blocking in your own application code or integration. You can also monitor your current usage from your <Anchor target="_blank" href="https://app.rentcast.io/app/api">API dashboard</Anchor> and will receive email notifications when you reach 85% and 100% of your monthly API request limit.

<br />

**Where can I view and track my API usage?**

You can view your API usage, the number of requests you have made during the current billing period, as well as any accumulated overage fees on your <Anchor target="_blank" href="https://app.rentcast.io/app/api">API dashboard</Anchor>.

<br />

**Will I get a notification when I'm close to exceeding my plan's monthly API request limit?**

Yes, you will receive an automated email notification when you reach 85% of your current month's API request limit, and another when you reach 100%.

Check your spam or junk mail folder if you don't see these notification emails in your inbox, and add our <Anchor target="_blank" href="https://rentcast.io">rentcast.io</Anchor> domain to your allowed senders list.

<br />

**When will I be billed and charged for my API subscription?**

Our billing system will generate an invoice and charge your saved payment method each month, on the same day of the month that you first activated your current API plan and subscription.

Each invoice will include a monthly charge for your current API plan, as well as a charge for any overage fees you have accumulated over the previous month. You will receive each invoice via email, and you can download past invoices and receipts from the <Anchor target="_blank" href="https://app.rentcast.io/app/account/billing">billing page</Anchor> in your account settings.

If you accumulate a large amount of overage fees over the course of a month, our billing system may generate additional invoices and charges for these fees in the middle of your regular billing period.

<br />

**I have other questions, who can I speak with regarding billing or pricing?**

You can send us any questions you have about billing or pricing [via email](mailto:support@rentcast.io), or use the live chat button at the bottom right of our website to speak with our team.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>