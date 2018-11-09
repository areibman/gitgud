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
    title: "rowTitle 0"
  },
  {
    title: "rowTitle 1"
  },
  {
    title: "rowTitle 2"
  },
  {
    title: "rowTitle 3"
  }
];

export class DataContainer extends React.PureComponent {
  renderRows = () => {
    return this.props.requestedData.map((row, index) => {
      console.log(row);
      return (
        <DataRow
          loadAsOpen={index === 0 ? true : false}
          key={row.key}
          title={row.key}
          svgs={row.svgs}
        />
      );
    });
  };

  render() {
    return (
      <Container>
        <ScrollContainer>
          {this.props.showSearch
            ? this.renderRows()
            : this.props.noResults
              ? "No results found."
              : ""}
        </ScrollContainer>
      </Container>
    );
  }
}
