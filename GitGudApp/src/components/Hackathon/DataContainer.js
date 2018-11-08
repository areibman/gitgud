import * as React from "react";
import styled from "styled-components";
import { DataRow } from "./DataRow";

const Container = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  overflow-x: hidden;
  overflow-y: scroll;
  padding: 10px;
  height: 100%;
`;

const ScrollContainer = styled.div``;
const fakeRowData = [
  {
    title: "rowTitle 0",
    data1: 11,
    data2: "data 2 0"
  },
  {
    title: "rowTitle 1",
    data1: 11,
    data2: "data 2 1"
  },
  {
    title: "rowTitle 2",
    data1: 11,
    data2: "data 2 2"
  },
  {
    title: "rowTitle 3",
    data1: 11,
    data2: "data 2 3"
  }
];

// noResults
// hasActiveSearch
export class DataContainer extends React.PureComponent {
  state = {};

  renderRows = () => {
    return fakeRowData.map((row, index) => {
      return (
        <DataRow
          loadAsOpen={index === 0 ? true : false}
          key={row.title}
          row={row}
        />
      );
    });
  };

  render() {
    return (
      <Container>
        <ScrollContainer>
          {this.props.showSearch || true
            ? this.renderRows()
            : this.props.noResults
              ? "No results found."
              : ""}
        </ScrollContainer>
      </Container>
    );
  }
}
