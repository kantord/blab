(window.webpackJsonp=window.webpackJsonp||[]).push([[15],{32:function(e,t,c){"use strict";
/*! js-cookie v3.0.1 | MIT */function n(e){for(var t=1;t<arguments.length;t++){var c=arguments[t];for(var n in c)e[n]=c[n]}return e}var r=function e(t,c){function r(e,r,b){if("undefined"!=typeof document){"number"==typeof(b=n({},c,b)).expires&&(b.expires=new Date(Date.now()+864e5*b.expires)),b.expires&&(b.expires=b.expires.toUTCString()),e=encodeURIComponent(e).replace(/%(2[346B]|5E|60|7C)/g,decodeURIComponent).replace(/[()]/g,escape);var o="";for(var s in b)b[s]&&(o+="; "+s,!0!==b[s]&&(o+="="+b[s].split(";")[0]));return document.cookie=e+"="+t.write(r,e)+o}}return Object.create({set:r,get:function(e){if("undefined"!=typeof document&&(!arguments.length||e)){for(var c=document.cookie?document.cookie.split("; "):[],n={},r=0;r<c.length;r++){var b=c[r].split("="),o=b.slice(1).join("=");try{var s=decodeURIComponent(b[0]);if(n[s]=t.read(o,s),e===s)break}catch(e){}}return e?n[e]:n}},remove:function(e,t){r(e,"",n({},t,{expires:-1}))},withAttributes:function(t){return e(this.converter,n({},this.attributes,t))},withConverter:function(t){return e(n({},this.converter,t),this.attributes)}},{attributes:{value:Object.freeze(c)},converter:{value:Object.freeze(t)}})}({read:function(e){return'"'===e[0]&&(e=e.slice(1,-1)),e.replace(/(%[\dA-F]{2})+/gi,decodeURIComponent)},write:function(e){return encodeURIComponent(e).replace(/%(2[346BF]|3[AC-F]|40|5[BDE]|60|7[BCD])/g,decodeURIComponent)}},{path:"/"});t.a=r},35:function(e,t,c){"use strict";var n=c(0);function r(e){Object(n.h)(e,"svelte-siteg8",".content.svelte-siteg8:not(:last-child){margin-bottom:1.5rem}")}function b(e){let t,c;const r=e[1].default,b=Object(n.z)(r,e,e[0],null);return{c(){t=Object(n.D)("div"),b&&b.c(),this.h()},l(e){t=Object(n.p)(e,"DIV",{class:!0});var c=Object(n.n)(t);b&&b.l(c),c.forEach(n.C),this.h()},h(){Object(n.j)(t,"class","content svelte-siteg8")},m(e,r){Object(n.O)(e,t,r),b&&b.m(t,null),c=!0},p(e,[t]){b&&b.p&&(!c||1&t)&&Object(n.pb)(b,r,e,e[0],c?Object(n.I)(r,e[0],t,null):Object(n.H)(e[0]),null)},i(e){c||(Object(n.mb)(b,e),c=!0)},o(e){Object(n.nb)(b,e),c=!1},d(e){e&&Object(n.C)(t),b&&b.d(e)}}}function o(e,t,c){let{$$slots:n={},$$scope:r}=t;return e.$$set=e=>{"$$scope"in e&&c(0,r=e.$$scope)},[r,n]}class s extends n.b{constructor(e){super(),Object(n.N)(this,e,o,b,n.bb,{},r)}}t.a=s},467:function(e,t,c){"use strict";c.r(t),c.d(t,"preload",(function(){return o}));var n=c(0),r=c(49);function b(e){let t,c;return t=new r.a({props:{readmeHTML:e[0],title:"Terms of Service"}}),{c(){Object(n.w)(t.$$.fragment)},l(e){Object(n.o)(t.$$.fragment,e)},m(e,r){Object(n.S)(t,e,r),c=!0},p(e,[c]){const n={};1&c&&(n.readmeHTML=e[0]),t.$set(n)},i(e){c||(Object(n.mb)(t.$$.fragment,e),c=!0)},o(e){Object(n.nb)(t.$$.fragment,e),c=!1},d(e){Object(n.A)(t,e)}}}async function o(){return{readmeHTML:await Object(r.b)(await c.e(160).then(c.bind(null,457)))}}function s(e,t,c){let{readmeHTML:n}=t;return e.$$set=e=>{"readmeHTML"in e&&c(0,n=e.readmeHTML)},[n]}class i extends n.b{constructor(e){super(),Object(n.N)(this,e,s,b,n.bb,{readmeHTML:0})}}t.default=i},49:function(e,t,c){"use strict";c.d(t,"b",(function(){return a}));var n=c(0),r=c(36),b=c(35);function o(e){let t;return{c(){t=Object(n.D)("meta"),this.h()},l(e){t=Object(n.p)(e,"META",{name:!0,content:!0}),this.h()},h(){Object(n.j)(t,"name","description"),Object(n.j)(t,"content",e[2])},m(e,c){Object(n.O)(e,t,c)},p(e,c){4&c&&Object(n.j)(t,"content",e[2])},d(e){e&&Object(n.C)(t)}}}function s(e){let t,c;return{c(){t=new n.a,c=Object(n.E)(),this.h()},l(e){t=Object(n.q)(e),c=Object(n.E)(),this.h()},h(){t.a=c},m(r,b){t.m(e[0],r,b),Object(n.O)(r,c,b)},p(e,c){1&c&&t.p(e[0])},d(e){e&&Object(n.C)(c),e&&t.d()}}}function i(e){let t,c,i,a,j,l,O,u,d,p,f,m,h,$,g;document.title=t=e[1];let v=e[2]&&o(e);a=new r.a({});const w=e[3].default,C=Object(n.z)(w,e,e[4],null);return $=new b.a({props:{$$slots:{default:[s]},$$scope:{ctx:e}}}),{c(){v&&v.c(),c=Object(n.E)(),i=Object(n.hb)(),Object(n.w)(a.$$.fragment),j=Object(n.hb)(),l=Object(n.D)("section"),O=Object(n.D)("div"),u=Object(n.D)("div"),d=Object(n.D)("h1"),p=Object(n.kb)(e[1]),f=Object(n.hb)(),m=Object(n.D)("div"),C&&C.c(),h=Object(n.hb)(),Object(n.w)($.$$.fragment),this.h()},l(t){const r=Object(n.Z)('[data-svelte="svelte-18pdwex"]',document.head);v&&v.l(r),c=Object(n.E)(),r.forEach(n.C),i=Object(n.r)(t),Object(n.o)(a.$$.fragment,t),j=Object(n.r)(t),l=Object(n.p)(t,"SECTION",{class:!0});var b=Object(n.n)(l);O=Object(n.p)(b,"DIV",{class:!0});var o=Object(n.n)(O);u=Object(n.p)(o,"DIV",{class:!0});var s=Object(n.n)(u);d=Object(n.p)(s,"H1",{class:!0});var g=Object(n.n)(d);p=Object(n.s)(g,e[1]),g.forEach(n.C),f=Object(n.r)(s),m=Object(n.p)(s,"DIV",{class:!0});var w=Object(n.n)(m);C&&C.l(w),h=Object(n.r)(w),Object(n.o)($.$$.fragment,w),w.forEach(n.C),s.forEach(n.C),o.forEach(n.C),b.forEach(n.C),this.h()},h(){Object(n.j)(d,"class","title"),Object(n.j)(m,"class","section box"),Object(n.j)(u,"class","container"),Object(n.j)(O,"class","hero-body"),Object(n.j)(l,"class","hero is-primary md-page")},m(e,t){v&&v.m(document.head,null),Object(n.g)(document.head,c),Object(n.O)(e,i,t),Object(n.S)(a,e,t),Object(n.O)(e,j,t),Object(n.O)(e,l,t),Object(n.g)(l,O),Object(n.g)(O,u),Object(n.g)(u,d),Object(n.g)(d,p),Object(n.g)(u,f),Object(n.g)(u,m),C&&C.m(m,null),Object(n.g)(m,h),Object(n.S)($,m,null),g=!0},p(e,[r]){(!g||2&r)&&t!==(t=e[1])&&(document.title=t),e[2]?v?v.p(e,r):(v=o(e),v.c(),v.m(c.parentNode,c)):v&&(v.d(1),v=null),(!g||2&r)&&Object(n.eb)(p,e[1]),C&&C.p&&(!g||16&r)&&Object(n.pb)(C,w,e,e[4],g?Object(n.I)(w,e[4],r,null):Object(n.H)(e[4]),null);const b={};17&r&&(b.$$scope={dirty:r,ctx:e}),$.$set(b)},i(e){g||(Object(n.mb)(a.$$.fragment,e),Object(n.mb)(C,e),Object(n.mb)($.$$.fragment,e),g=!0)},o(e){Object(n.nb)(a.$$.fragment,e),Object(n.nb)(C,e),Object(n.nb)($.$$.fragment,e),g=!1},d(e){v&&v.d(e),Object(n.C)(c),e&&Object(n.C)(i),Object(n.A)(a,e),e&&Object(n.C)(j),e&&Object(n.C)(l),C&&C.d(e),Object(n.A)($)}}}async function a(e){const t=await Promise.all([c.e(2),c.e(17)]).then(c.t.bind(null,62,7)),n=await c.e(2).then(c.t.bind(null,58,7)),r=await c.e(18).then(c.t.bind(null,68,7)),b=await c.e(19).then(c.t.bind(null,72,7)),o=c.e(20).then(c.bind(null,74));return(await t.default().use(n.default,{gfm:!0,commonmark:!0}).use(b.default).use(o.default).use(r.default).process(e.default)).contents}function j(e,t,c){let{$$slots:n={},$$scope:r}=t,{readmeHTML:b}=t,{title:o}=t,{description:s=null}=t;return e.$$set=e=>{"readmeHTML"in e&&c(0,b=e.readmeHTML),"title"in e&&c(1,o=e.title),"description"in e&&c(2,s=e.description),"$$scope"in e&&c(4,r=e.$$scope)},[b,o,s,n,r]}class l extends n.b{constructor(e){super(),Object(n.N)(this,e,j,i,n.bb,{readmeHTML:0,title:1,description:2})}}t.a=l}}]);