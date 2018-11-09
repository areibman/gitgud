import * as React from "react";
import styled from "styled-components";
import { DataRow } from "./DataRow";

const Container = styled.div`
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  width: 100%;
  overflow-x: hidden;
  overflow-y: scroll;
  padding: 10px;
  height: 100%;
  svg {
    width: 100%;
    height: 350px;
  }
`;

const ScrollContainer = styled.div``;

export class DataContainer extends React.PureComponent {
  renderRows = () => {
    return this.props.requestedData ? (
      this.props.requestedData.map((row, index) => {
        return (
          <DataRow
            loadAsOpen={index === 0 ? true : false}
            key={row.key}
            title={row.key}
            svgs={row.svgs}
          />
        );
      })
    ) : (
      <span>
        {" "}
        No data for (your champ || that champ). I don't care to check which. Go
        away.
      </span>
    );
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
