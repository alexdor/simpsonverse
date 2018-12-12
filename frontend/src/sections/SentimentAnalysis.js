import React, { memo } from "react";

import SenAn from "../data/normalizedHappinessScores.json";

const SentimentAnalysis = () => (
  <div className="row no-gutters d-flex">
    {SenAn.map(char => (
      <div key={char[0]} className="col-6 col-md-3">
        <div className="card-flip">
          <div className="d-flex flex-column align-items-center justify-content-center char-wrapper flip">
            <div className="front">
              <div className="card">
                <div className="card-block simpson-pic ">
                  <img
                    src={`${process.env.PUBLIC_URL}/character_pictures/${
                      char[0]
                    }.png`}
                    alt={char[0]}
                    className="img-fluid"
                  />
                </div>{" "}
              </div>
            </div>
            <div className="char-info back">
              <div className="card">
                <div className="card-block">
                  <p className="text-capitalize">{char[0]}</p>
                  <p style={{ color: char[1] > 50 ? "green" : "red" }}>
                    {char[1]}%
                  </p>
                </div>
              </div>
            </div>
          </div>{" "}
        </div>
      </div>
    ))}
  </div>
);

export default memo(SentimentAnalysis);
