import * as React from "react";
import styled from "styled-components";
import { DataRow } from "./DataRow";
import background from "../../assets/background.jpg";
import { transparentize } from "polished";

const Container = styled.div`
  width: 100%;
  overflow-x: hidden;
  overflow-y: scroll;
  padding: 10px;
  height: 100%;
  svg {
    width: 100%;
    height: 350px;
  }
  background-image: url(${background});
`;

const ScrollContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  background-color: ${props => (props.bg ? transparentize(0.2, "white") : "")};
  border-radius: 4px;
`;

const ErrorText = styled.span`
  font-size: 18px;
  color: white;
`;

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
    ) : !this.props.loading ? (
      <span>
        No data for (your champ || that champ). I don't care to check which. Go
        away.
      </span>
    ) : null;
  };

  render() {
    return (
      <Container>
        <ScrollContainer bg={this.props.showSearch}>
          {this.props.showSearch ? (
            this.renderRows()
          ) : !this.props.loading ? (
            <ErrorText>
              Please select a summoner, champion, and region.
            </ErrorText>
          ) : null}
        </ScrollContainer>
      </Container>
    );
  }
}
