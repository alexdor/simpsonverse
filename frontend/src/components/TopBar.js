import React, { PureComponent } from "react";
import {
  Collapse,
  Nav,
  Navbar,
  NavbarBrand,
  NavbarToggler,
  NavItem,
  NavLink
} from "reactstrap";

import Logo from "./logo.png";

const scrollTo = name => e => {
  e.preventDefault();
  window.scrollTo({
    top: document.getElementById(name).offsetTop,
    behavior: "smooth"
  });
};

export default class Example extends PureComponent {
  state = {
    isOpen: false
  };
  toggle = () => {
    this.setState(state => ({
      isOpen: !state.isOpen
    }));
  };
  render() {
    return (
      <div>
        <Navbar color="light" light expand="md">
          <div className="row no-gutters w-100">
            <div className="col-auto col-md-12 mr-auto row justify-content-center no-gutters">
              <NavbarBrand className="mx-auto" href="/">
                <img src={Logo} alt="logo" className="img-fluid logo" />
              </NavbarBrand>
            </div>
            <div className="col-auto col-md-12 ">
              <NavbarToggler className="ml-auto" onClick={this.toggle} />
              <Collapse isOpen={this.state.isOpen} navbar>
                <Nav className="d-flex mx-auto my-3" navbar>
                  <NavItem>
                    <NavLink href="" onClick={scrollTo("SimpsonsFacebook")}>
                      The Simpson{"'"}s Facebook
                    </NavLink>
                  </NavItem>
                  <NavItem>
                    <NavLink href="" onClick={scrollTo("AppearancesNetwork")}>
                      Appearances Network
                    </NavLink>
                  </NavItem>
                  <NavItem>
                    <NavLink href="" onClick={scrollTo("WordClouds")}>
                      Word Clouds
                    </NavLink>
                  </NavItem>
                  <NavItem>
                    <NavLink href="" onClick={scrollTo("SentimentAnalysis")}>
                      Sentiment Analysis
                    </NavLink>
                  </NavItem>
                </Nav>
              </Collapse>
            </div>
          </div>
        </Navbar>
      </div>
    );
  }
}
