import * as React from "react";
import styled from "styled-components";
import { Collapse } from "react-collapse";

const RowContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  border: 1px solid #008cba;
  border-radius: 4px;
  margin-bottom: 10px;
  padding: 10px;
  color: darkgrey;
`;

const InnerRow = styled.div`
  display: flex;
`;

const RowItem = styled.div`
  width: 100%;
`;

const Expander = styled.span`
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
`;

const FakeGraph = styled.div`
  min-width: 250px;
  min-height: 250px;
  background-color: rebeccaPurple;
`;
// props
// row
// loadAsOpen
export class DataRow extends React.PureComponent {
  state = {
    expanded: this.props.loadAsOpen
  };

  toggleCollapse = () => {
    this.setState({ expanded: !this.state.expanded });
  };

  render() {
    const { title, data1, data2 } = this.props.row;

    return (
      <RowContainer>
        <InnerRow>
          <RowItem>{title}</RowItem>
          <Expander onClick={this.toggleCollapse}>
            {this.state.expanded ? "-" : "+"}
          </Expander>
        </InnerRow>
        <Collapse isOpened={this.state.expanded}>
          <InnerRow>
            <RowItem>{data1}</RowItem>
            <RowItem>{data2}</RowItem>
          </InnerRow>
          <InnerRow>
            <FakeGraph />
          </InnerRow>
          <InnerRow>
            <RowItem>{data1}</RowItem>
            <RowItem>{data2}</RowItem>
          </InnerRow>
        </Collapse>
      </RowContainer>
    );
  }
}
