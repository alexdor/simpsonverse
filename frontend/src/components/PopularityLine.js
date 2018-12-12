import React, { PureComponent } from "react";
import { defaults, Line } from "react-chartjs-2";
import Select from "react-select";

import popularity from "../data/popularity.json";
import { customStyles, options } from "../helpers/helpers.js";

defaults.global.animation.duration = 300;
defaults.global.legend.position = "bottom";
defaults.global.tooltips.mode = "point";
defaults.global.tooltips.backgroundColor = "#fff";
defaults.global.tooltips.bodyFontColor = "#000";
defaults.global.tooltips.titleFontColor = "#000";
const colorMap = new Map();
const dynamicColors = value => {
  if (colorMap.has(value)) {
    return colorMap.get(value);
  }
  const r = Math.floor(Math.random() * 255);
  const g = Math.floor(Math.random() * 255);
  const b = Math.floor(Math.random() * 255);
  const rgb = "rgb(" + r + "," + g + "," + b + ")";
  colorMap.set(value, rgb);
  return rgb;
};
const seasons = options.map(op => op.label);
const popularityOptions = Object.keys(popularity).map(el => ({
  label: el,
  value: el
}));

export default class PopularityLine extends PureComponent {
  state = {
    selectedPopOption: popularityOptions[0],
    loadingPop: false,
    data: {
      labels: seasons,
      datasets: [
        {
          label: popularityOptions[0].value,
          data: popularity[popularityOptions[0].value],
          borderWidth: 1,
          fill: false,
          borderColor: dynamicColors(popularityOptions[0].value)
        }
      ]
    }
  };

  handlePopChange = (selectedPopOption = []) => {
    this.setState(state => ({
      data: {
        labels: state.data.labels,
        datasets: selectedPopOption.map(opt => ({
          borderWidth: 1,
          data: popularity[opt.value],
          label: opt.value,
          fill: false,
          borderColor: dynamicColors(opt.value)
        }))
      },
      selectedPopOption
    }));
  };

  render() {
    const { selectedPopOption, data } = this.state;
    return (
      <div className="mx-4">
        <h4 className="d-flex justify-content-center mx-auto">
          Select one or more characters to view their popularity across the
          seasons
        </h4>
        <Select
          isSearchable
          isMulti
          styles={customStyles}
          value={selectedPopOption}
          onChange={this.handlePopChange}
          options={popularityOptions}
        />
        <Line data={data} options={{ maintainAspectRatio: false }} />
      </div>
    );
  }
}
