import React from "react";
import { Button, Form, FormGroup, Input, Label } from "reactstrap";

import axios from "axios";

import { API_PORTFOLIO_URL } from "../constants";

class NewPortfolioForm extends React.Component {
  state = {
    pk: 0,
    name: "",
    description: ""
  };

  componentDidMount() {
    if (this.props.portfolio) {
      const { pk, name, description } = this.props.portfolio;
      this.setState({ pk, name, description });
    }
  }

  onChange = e => {
    this.setState({ [e.target.name]: e.target.value });
  };

  createPortfolio = e => {
    e.preventDefault();
    axios.post(API_PORTFOLIO_URL, this.state).then(() => {
      this.props.resetState();
      this.props.toggle();
    });
  };

  editPortfolio = e => {
    e.preventDefault();
    axios.put(API_PORTFOLIO_URL + this.props.portfolio.id, this.state).then(() => {
      this.props.resetState();
      this.props.toggle();
    });
  };

  defaultIfEmpty = value => {
    return value === "" ? "" : value;
  };

  render() {
    return (
      <Form onSubmit={this.props.portfolio ? this.editPortfolio : this.createPortfolio}>
        <FormGroup>
          <Label for="name">Name:</Label>
          <Input
            type="text"
            name="name"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.name)}
          />
        </FormGroup>
        <FormGroup>
          <Label for="description">Description:</Label>
          <Input
            type="text"
            name="description"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.description)}
          />
        </FormGroup>
        <Button>Send</Button>
      </Form>
    );
  }
}

export default NewPortfolioForm;