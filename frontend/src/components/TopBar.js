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
import scrollToElement from "scroll-to-element";

import Logo from "./logo.png";

const scrollTo = name => () => {
  return scrollToElement(`#${name}`, {
    offset: 0,
    ease: "out-bounce",
    duration: 500
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
                  <NavItem onClick={scrollTo("SimpsonsFacebook")}>
                    <NavLink href="#SimpsonsFacebook">
                      The Simpson{"'"}s Facebook
                    </NavLink>
                  </NavItem>
                  <NavItem onClick={scrollTo("AppearancesNetwork")}>
                    <NavLink href="#AppearancesNetwork">
                      Appearances Network
                    </NavLink>
                  </NavItem>
                  <NavItem onClick={scrollTo("WordClouds")}>
                    <NavLink href="#WordClouds">Word Clouds</NavLink>
                  </NavItem>
                  <NavItem onClick={scrollTo("SentimentAnalysis")}>
                    <NavLink href="#SentimentAnalysis">
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
