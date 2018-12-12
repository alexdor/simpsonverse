import "./App.scss";

import React, { lazy, PureComponent, StrictMode, Suspense } from "react";

import SectionHeader from "./components/SectionHeader";
import Spinner from "./components/Spinner";
import TopBar from "./components/TopBar";

const sections = [
  {
    key: "SimpsonsFacebook",
    Component: lazy(() => import("./sections/SimpsonsFacebook")),
    title: "Simpson's Facebook",
    subtitle:
      "Have you ever wondered what Facebook would have looked like in the Simpsons universe? We've done the work, so you can find out! Below is an interactive network that illustrates each character as a node. Based on the character's wiki page, links to other nodes are created based on who is mentioned. In addition to being able to move the nodes below, hovering over a node will reveal the corresponding character."
  },
  {
    key: "AppearancesNetwork",
    Component: lazy(() => import("./sections/AppearancesNetwork")),
    title: "Appearances Network",
    subtitle:
      "Consequently, we wanted to see what network would be created if we based the network connections on who appeared the same episodes. For each episode 2 characters appears in, the strength of their connection increased. Scroll through the seasons to see how the networks evolved throughout the show! "
  },
  {
    key: "WordClouds",
    Component: lazy(() => import("./sections/WordClouds")),
    title: "Word Clouds",
    subtitle:
      "When The Simpsons is mentioned in conversation, yellow people and funny lines come to mind. To catch the most iconic quotes from each character and present them in a pleasing fashion, we created some word clouds for you enjoyment! Check out the word clouds we generated for the Simpsons family!"
  },
  {
    key: "SentimentAnalysis",
    Component: lazy(() => import("./sections/SentimentAnalysis")),
    title: "Sentiment Analysis",
    subtitle:
      "The Simpsons is a show full of gags, tender moments, dastardly drama, and angry tirades. To figure out which characters are the most positive and the most negative, we implemented sentimental analysis to determine if each character is more hero or villain, clown or...sad clown. After accumulating the scores for all of each character's quotes, we normalized the range and gave each character a percentage ranking. The higher the score, the more positive the overall quote collection. The lower, the more negative. Check out a sample of the rankings below!"
  }
];

class App extends PureComponent {
  render() {
    return [
      <TopBar key="topbar" />,
      <div className="section-wrapper" key="div">
        <StrictMode>
          {sections.map(({ key, Component, title, subtitle }, index) => (
            <div
              id={key}
              key={key}
              className={`section pb-2 ${index % 2 ? "blue" : ""}`}
            >
              <SectionHeader title={title} subtitle={subtitle} />
              <Suspense fallback={<Spinner />}>
                <Component />
              </Suspense>
            </div>
          ))}
        </StrictMode>
      </div>,
      <h2 className="my-5 text-center" key="forg">
        Don{"'"}t forget to check our python notebook for more info, you can
        find it{" "}
        <a
          target="_blank"
          rel="noopener noreferrer"
          href="https://nbviewer.jupyter.org/github/alexdor/simpsonverse/blob/master/Final%20Project.ipynb"
        >
          here
        </a>
      </h2>
    ];
  }
}

export default App;
