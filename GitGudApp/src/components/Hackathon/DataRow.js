import * as React from "react";
import styled from "styled-components";

const RowItem = styled.div`
  width: 50%;
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
