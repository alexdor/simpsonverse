import React, { PureComponent } from "react";
import { defaults, Line } from "react-chartjs-2";
import Select from "react-select";

import popularity from "../data/popularity.json";
import { customStyles, options } from "../helpers/helpers.js";

defaults.global.animation.duration = 300;

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
          borderWidth: 1
        }
      ]
    }
  };

  handlePopChange = selectedPopOption => {
    if (selectedPopOption.value) {
      if (
        (this.state.selectedPopOption || {}).value !== selectedPopOption.value
      ) {
        this.setState(state => ({
          data: {
            labels: state.data.labels,
            datasets: [
              {
                ...state.data.datasets[0],
                data: popularity[selectedPopOption.value],
                label: selectedPopOption.value
              }
            ]
          },
          selectedPopOption
        }));
      }
    }
  };
  render() {
    const { selectedPopOption, data } = this.state;
    return (
      <div>
        <h4 className="d-flex justify-content-center mx-auto">
          Select a character to view his popularity across the seasons
        </h4>
        <Select
          isSearchable
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
