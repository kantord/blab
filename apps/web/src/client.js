import * as sapper from "@sapper/app"
import "./mystyles.scss"
import "./i18n"
import { library, dom } from "@fortawesome/fontawesome-svg-core"
import {
  faVolumeUp,
  faCheckSquare,
  faDumbbell,
  faStar,
  faUser,
  faLock,
  faEnvelope,
  faHeart,
  faSpinner,
} from "@fortawesome/free-solid-svg-icons"
import { faTwitter } from "@fortawesome/free-brands-svg-icons"
import { worker } from "./mocks/browser"

library.add(faVolumeUp)
library.add(faCheckSquare)
library.add(faDumbbell)
library.add(faTwitter)
library.add(faStar)
library.add(faUser)
library.add(faLock)
library.add(faEnvelope)
library.add(faHeart)
library.add(faSpinner)
dom.watch()

// Intercept certain HTTP requests
worker.start()

sapper.start({
  target: document.querySelector("#sapper"),
})

if (!window.isCypress) {
  require("@openfonts/noto-sans_all")
}
