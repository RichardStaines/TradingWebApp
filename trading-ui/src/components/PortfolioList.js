import React, { Component } from "react";
import { Table } from "reactstrap";
import NewPortfolioModal from "./NewPortfolioModal";

import ConfirmRemovalModal from "./ConfirmRemovalModal";

class PortfolioList extends Component {
  render() {
    const portfolios = this.props.portfolios;
    return (
      <Table dark>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Created On</th>
            <th>Updated On</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {!portfolios || portfolios.length <= 0 ? (
            <tr>
              <td colSpan="3" align="center">
                <b>Ops, no one here yet</b>
              </td>
            </tr>
          ) : (
            portfolios.map(portfolio => (
              <tr key={portfolio.id}>
                <td>{portfolio.id} / {portfolio.name}</td>
                <td>{portfolio.description}</td>
                <td>{portfolio.created_on}</td>
                <td>{portfolio.updated_on}</td>
                <td align="center">
                  <NewPortfolioModal
                    create={false}
                    portfolio={portfolio}
                    resetState={this.props.resetState}
                  />
                  &nbsp;&nbsp;
                  <ConfirmRemovalModal
                    pk={portfolio.id}
                    resetState={this.props.resetState}
                  />
                </td>
              </tr>
            ))
          )}
        </tbody>
      </Table>
    );
  }
}

export default PortfolioList;
