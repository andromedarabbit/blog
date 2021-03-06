---
date: 2020-04-14
syndicated:
- type: mastodon
  url: https://mastodon.technology/users/roytang/statuses/103994779577322470
- type: twitter
  url: https://twitter.com/roytang/statuses/1249900205387857921/
tags:
- software development
title: Bespoke vs Product Development
---

For most of my time working on software projects, it has always been for bespoke projects. Bespoke basically means a software program or package tailor-made for a specific client. The client provides all the requirements, the team fleshes out more details and specifications, some prototyping may or may not ensure, and implementation proceeds thusly. It’s relatively straightforward compared to product development.

I only started getting involved with “product”-like projects over the in the latter half of my career as a software developer. A "product" is a more general use software program or package, perhaps sold to the mass market or as a service. My experience is mostly with products that are targeted towards the public sector (government agencies and such) and not for general consumer use. Though I imagine many similar issues and pitfalls as I discuss here can occur in other types of product development as well. These are largely issues of "building for multiple clients" as opposed to "building for a specific client".

The project lifecycle is markedly different: you start with an idea for a product, perhaps based on something you’ve already built before, and shop it around to potential clients who could use such a system. A number of clients put out tenders for projects where they specify it has to be a pre-built product instead of a bespoke solution. Typically you use the requirements from these tenders to direct your development while you don’t have clients signed up yet. That’s right, you start development work ahead of time even when you don’t have clients signed up yet. These tenders typically have significant lead time before the actual implementation, so you kind of hope that if you somehow magically win with your proposal, you have everything (or at least most of it) done and in place and ready for the client. 

Tenders can also sometimes have a requirement to have a demonstration during the tendering process. Therein lies the first problem - since you probably don’t have the product ready yet, there’s probably some crunch time needed in preparing and setting up the demo. Some iffy code will need to be written, sacrificing code quality and maintainability in order to meet the timescales for the demo.

Of course, since you want to gain traction as quickly as possible, you try to shop around to as many clients as you can. That means you try to bid for as many tenders as you can, and different clients can have different requirements. This of course creates more problems for the development team in the form of conflicting requirements and even worse, possibly conflicting demo schedules. It’s something that management has to be cognizant of and the company will need to pick and choose its battles. Poorly handled, it could put a lot of pressure on the development team.

I was discussing this the other day with a younger developer working in another company. They were working on a project that was headed in this direction and he was asking whether things would get better once they have more things, and I kind of laughed a little bit before telling him there’s a good chance it would get worse. 

The problem of conflicting requirements gets even more complicated when the clients are actually paying for your product because now you have even more responsibility to fulfill their custom requirements. One would think that if you were making an off the shelf product you’re not really subject to the whims of the clients too much, but when you’re trying to gain traction in an existing market you will sometimes need to make compromises to get clients to choose you over more established products, which probably means catering more to their whims. 

And really, even clients in the same space needing the same product will have their own requirements, idiosyncrasies and ways of doing things. Sometimes even when there are statutes in place dictating standards (like what data should be recorded and so on), different clients will still have different ways of meeting those standards such that your system may not be able to cater for all of the differences.

Ideally, your product has been planned with such variations in requirements in mind. This means making your system flexible and/or configurable enough to handle any differences between clients, or at least changes can be kept small and manageable between clients. This assumes of course that you had the foresight to predict ahead of time what the differences would be and planned your system architecture accordingly, and that you didn’t have a lot of poor and hard-to-maintain code littered throughout your system because of needing to meet conflicting demo requirements! The more customizable your system needs to be, the more well-structured, modular and lightly coupled the code has to be. 

If you don’t have the above, well then likely you’re looking at introducing even more bad code and stretching your code base with code smells everywhere in order to accommodate tight deadlines and conflicting requirements.

There’s also a lot more that would need to be customizable than you might expect. Some things that clients want tailored for their needs are: UI theme or individual UI elements; menu structures; field names and error messages; message/email/notification templates; access control rights; form layouts, what fields are included in each form, field validation logic; reports, what fields are included, and even retrieval logic. These are just some examples, there are many more that are difficult to foresee just how the clients might want them customized, so most likely even with the best-designed system there will still need to be some level of customization done for each client.

How to avoid such pitfalls? It helps if your product has a strong identity and design from the very start, but that means having a strong product manager or management team with a good understanding of the domain required for your system. The product manager will need to manage the clients’ requirements and the direction of future development. The product manager has to be able to assess the client requests and say “no, that’s not how our product works,” when faced with requests that will make things more complicated for the development team.

The above are drawn from my personal experience and from a few other developers’. I’m sure there are ways to handle product development to avoid these problems of course, but I believe that far more projects encounter these difficulties than do not, but it mostly comes down to management understanding the concerns and making adjustments to resources and schedules accordingly.