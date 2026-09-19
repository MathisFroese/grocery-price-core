# Accessibility and public benefit

## Who this is for

Grocery Price Core is a **developer library**, not a finished accessible app or a clinical tool. Its public purpose is to provide dependable pricing primitives for applications that help people with grocery shopping, budgeting and everyday planning.

One important motivation is the experience of people with **autism spectrum conditions, including people who identify with the term Asperger's, and people with ADHD**. They are not a single user group with identical needs. Some may benefit from fewer ambiguous choices, more predictable information, explicit price provenance and less manual comparison when energy or executive-function capacity is limited. The same design can help people with other disabilities, caring responsibilities, limited budgets or simply a busy day.

No diagnosis is needed to use applications built with this library, and there should be no requirement to disclose one. We encourage product teams to involve disabled people directly in testing rather than treating the library as proof that an app is accessible.

## The longer-term 360-degree workflow

The broader ambition is an application that supports the *whole* food routine rather than offering one more disconnected to-do list:

**Scan food → see fridge/pantry inventory and best-before dates → find recipes from what is available → make a flexible meal plan → identify missing ingredients → compare trustworthy local regular prices and offers → shop → update inventory.**

For people who find executive-function demands, switching between tasks, unpredictable changes or cognitive overload difficult, joining these steps could reduce repeated decisions. People differ: reminders, rewards, notification intensity, visual density and planning detail should be adjustable, and using the app should not require a diagnosis or a perfectly maintained inventory.

Grocery Price Core is the **publicly reusable price-information component** for developers exploring such experiences. It is not the full 360-degree application. Pantry scanning, recipe suggestions, inventory, meal planning, shopping interfaces and clinical/accessibility validation are outside the present library's scope. Any separate application and its source code may remain private.

## Why price semantics matter

A price comparison that labels an online pickup price as an in-store regular price can make a shopping plan unreliable. Presenting an unknown price as zero can produce misleading savings and unexpected costs. A price from an expired offer may create avoidable surprises.

This library makes these distinctions explicit in code:

| Situation | Library behavior | Potential user-facing benefit |
| --- | --- | --- |
| No verified price | Returns an unknown-price status, not a zero price | Less misleading certainty |
| Offer has expired | Declines to use it for current comparison | More predictable shopping |
| Pickup vs. in-store price | Requires an explicit cross-channel choice | Fewer hidden assumptions |
| Different package sizes | Normalizes mass, volume or piece prices | Less mental arithmetic |
| Estimates or last-paid amounts | Kept distinct from verified observations | More transparent budget information |

These are *possible benefits of applications built on top of this library*, not evidence that any disability-related outcomes have already been measured.

## Accessibility is a product responsibility

A downstream app should still test readability, keyboard and screen-reader use, clear language, adjustable notifications, low-stimulation presentation, recoverability after interrupted tasks, privacy and individual preferences. A back-end library alone cannot establish accessibility conformance.

## How to evaluate impact responsibly

With consent and suitable privacy protections, downstream projects could measure task completion, number of manual price corrections, participant-reported clarity, recovery after interruptions and unwanted surprises caused by missing or mismatched prices. Include disabled people with different needs in the design and evaluation. Do not assume one workflow works for all autistic people or everyone with ADHD.

The library is MIT-licensed. Its public benefit goal and the private status of any separate application do not change the license scope specified in [LICENSE](LICENSE).
