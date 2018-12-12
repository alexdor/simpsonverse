import React from "react";
import Bart from "../data/final_wordclouds/Bart_WordCloud.png";
import Homer from "../data/final_wordclouds/Homer_WordCloud.png";
import Lisa from "../data/final_wordclouds/Lisa_WordCloud.png";
import Marge from "../data/final_wordclouds/Marge_WordCloud.png";

const WordClouds = () => (
  <div className="row">
    <div className="col-12 col-md-6">
      <img className="img-fluid" alt="wordcloud for Bart" src={Bart} />
    </div>
    <div className="col-12 col-md-6">
      <img className="img-fluid" alt="wordcloud for Lisa" src={Lisa} />
    </div>
    <div className="col-12 col-md-6">
      <img className="img-fluid" alt="wordcloud for Marge" src={Marge} />
    </div>
    <div className="col-12 col-md-6">
      <img className="img-fluid" alt="wordcloud for Homert" src={Homer} />
    </div>
  </div>
);

export default WordClouds;
