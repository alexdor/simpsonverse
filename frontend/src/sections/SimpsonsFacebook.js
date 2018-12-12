import React, { PureComponent } from "react";

import FacebookData from "../data/SimpsonsFacebookCytoScape";
import { drawChart } from "../helpers/chartHelpers";

export default class SimpsonsFacebook extends PureComponent {
  componentDidMount = () => {
    drawChart("#simpsonFacebookGraph", FacebookData);
  };

  render() {
    return <div id="simpsonFacebookGraph" className="section-graph" />;
  }
}
