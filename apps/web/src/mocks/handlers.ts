import { rest } from "msw"
import ExampleGistResponse from "./__fixtures__/example-gist-response.json"
import { default as ExampleCourseDataFile } from "../courses/test/courseData.json"
import { default as TestCourseAnimalsSkillFile } from "../courses/test/challenges/animals.json"
import gistsConfig from "../../../../config/gists.json"

const FAKE_GIST_FILE = {
  filename: "hello",
  language: "json",
  raw_url:
    "https://gist.githubusercontent.com/asdf/2428349a05d81f96b2311c2749ea5c6d/raw/f9f8b9f9f9f9f9f9f9f9f9f9f9f9f9f9f9f9f9f/librelingo___courseData.ts",
  size: 5,
  type: "text/plain",
  truncated: false,
  content: "",
}

export const handlers = [
  rest.get(
    `${gistsConfig.baseURL}/db0545fc1ace67dd8c67d3bcae571b4442161060cd3cfc3890c55e351ec79245`,
    (req, res, ctx) => {
      return res(ctx.status(404), ctx.json({ error: "does not exist" }))
    }
  ),

  rest.get(
    `${gistsConfig.baseURL}/2428349a05d81f96b2311c2749ea5c6d`,
    (req, res, ctx) => {
      return res(
        ctx.json({
          ...ExampleGistResponse,
          files: {
            ...ExampleGistResponse.files,
            "librelingo___courseData.json": {
              ...FAKE_GIST_FILE,
              filename: "librelingo___courseData.json",
              content: JSON.stringify(ExampleCourseDataFile),
            },
            "librelingo___challenges___animals.json": {
              ...FAKE_GIST_FILE,
              filename: "librelingo___challenges___animals2.json",
              content: JSON.stringify(TestCourseAnimalsSkillFile),
            },
            "librelingo___introduction___animals.md": {
              ...FAKE_GIST_FILE,
              filename: "librelingo___introduction___animals.md",
              content: "hello world",
            },
          },
        })
      )
    }
  ),

  rest.get("*", (req) => {
    throw new Error(
      `Unhandled request: ${req.url}. All requests must be mocked in ${__filename}`
    )
  }),
]
