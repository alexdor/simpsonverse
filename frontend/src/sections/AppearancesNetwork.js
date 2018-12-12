import React, { PureComponent } from "react";
import Select from "react-select";

import PopularityLine from "../components/PopularityLine.js";
import Spinner from "../components/Spinner.js";
import data from "../data/season_appearances/Season1.json";
import { drawChart } from "../helpers/chartHelpers";
import { customStyles, options } from "../helpers/helpers.js";

export default class AppearancesNetwork extends PureComponent {
  state = {
    selectedOption: options[0],
    loading: false
  };

  componentDidMount() {
    drawChart("#ap", data, true);
  }

  handleChange = selectedOption => {
    if (selectedOption.value) {
      if ((this.state.selectedOption || {}).value !== selectedOption.value) {
        this.setState({
          selectedOption,
          loading: true
        });
        import(`../data/season_appearances/Season${
          selectedOption.value
        }.json`).then(data => {
          this.setState({ loading: false }, () =>
            drawChart("#ap", data.default, true)
          );
        });
      }
    }
  };

  render() {
    const { selectedOption, loading } = this.state;
    return (
      <div>
        <h4 className="d-flex justify-content-center mx-auto">
          Select a season that you would like to view
        </h4>
        <Select
          isSearchable
          styles={customStyles}
          value={selectedOption}
          onChange={this.handleChange}
          options={options}
        />
        {loading ? <Spinner /> : <div id="ap" className="section-graph" />}

        <PopularityLine />
      </div>
    );
  }
}
