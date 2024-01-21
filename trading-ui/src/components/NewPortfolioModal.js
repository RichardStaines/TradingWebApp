import React, { Component, Fragment } from "react";
import { Button, Modal, ModalHeader, ModalBody } from "reactstrap";
import NewPortfolioForm from "./NewPortfolioForm";

class NewPortfolioModal extends Component {
  state = {
    modal: false
  };

  toggle = () => {
    this.setState(previous => ({
      modal: !previous.modal
    }));
  };

  render() {
    const create = this.props.create;

    var title = "Editing Portfolio";
    var button = <Button onClick={this.toggle}>Edit</Button>;
    if (create) {
      title = "Creating New Portfolio";

      button = (
        <Button
          color="primary"
          className="float-right"
          onClick={this.toggle}
          style={{ minWidth: "200px" }}
        >
          Create New
        </Button>
      );
    }

    return (
      <Fragment>
        {button}
        <Modal isOpen={this.state.modal} toggle={this.toggle}>
          <ModalHeader toggle={this.toggle}>{title}</ModalHeader>

          <ModalBody>
            <NewPortfolioForm
              resetState={this.props.resetState}
              toggle={this.toggle}
              portfolio={this.props.portfolio}
            />
          </ModalBody>
        </Modal>
      </Fragment>
    );
  }
}

export default NewPortfolioModal;