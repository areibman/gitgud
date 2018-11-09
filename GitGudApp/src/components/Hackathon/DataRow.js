import * as React from "react";
import styled from "styled-components";
import { Collapse } from "react-collapse";
import { Scatter } from "react-chartjs-2";
import { darken } from "polished";

const RowContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  border: 1px solid #008cba;
  border-radius: 4px;
  margin-bottom: 10px;
  padding: 10px;
  color: darkgrey;
  background-color: #c5f1fa;
`;

const InnerRow = styled.div`
  display: flex;
  width: 100%;
`;

const RowItem = styled.div`
  width: 45%;
`;

const Expander = styled.span`
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
`;

const Title = styled.span`
  font-weight: bold;
  font-size: 24px;
  color: grey;
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

  renderSvgs = () => {
    return this.props.svgs.map((svg, index) => {
      return (
        <RowItem key={svg + index} dangerouslySetInnerHTML={{ __html: svg }} />
      );
    });
  };
  render() {
    return <React.Fragment>{this.renderSvgs()}</React.Fragment>;
  }
}
