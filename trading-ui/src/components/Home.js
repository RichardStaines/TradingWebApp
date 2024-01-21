import React, { Component } from "react";
import { Col, Container, Row } from "reactstrap";
import PortfolioList from "./PortfolioList";
import NewPortfolioModal from "./NewPortfolioModal";

import axios from "axios";

import { API_PORTFOLIOS_URL } from "../constants";

class Home extends Component {
  state = {
    portfolios: []
  };

  componentDidMount() {
    this.resetState();
  }

  getPortfolios = () => {
    axios.get(API_PORTFOLIOS_URL).then(res => this.setState({ portfolios: res.data }));
  };

  resetState = () => {
    this.getPortfolios();
  };

  render() {
    return (
      <Container style={{ marginTop: "20px" }}>
        <Row>
          <Col>
            <PortfolioList
              portfolios={this.state.portfolios}
              resetState={this.resetState}
            />
          </Col>
        </Row>
        <Row>
          <Col>
            <NewPortfolioModal create={true} resetState={this.resetState} />
          </Col>
        </Row>
      </Container>
    );
  }
}

export default Home;
