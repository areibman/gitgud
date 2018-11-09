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
  width: ${props => props.widthPercent || "100%"};
`;

const Expander = styled.span`
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
`;

const Title = styled.span`
  font-weight: bold;
  font-size: 24px;
  color: white;
  -webkit-text-stroke: 1px #008cba;
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

    var ajaxResponse = [
      { x: 60, y: 0.005 },
      { x: 80, y: 0.01 },
      { x: 90, y: 0.02 },
      { x: 111, y: 0.05 },
      { x: 114, y: 0.5 },
      { x: 160, y: 0.3 },
      { x: 180, y: 0.1 }
    ];

    const data = {
      datasets: [
        {
          label: "My First dataset",
          fill: true,
          lineTension: 0.1,
          backgroundColor: "#008cba",
          borderColor: darken(0.1, "#008cba"),
          borderCapStyle: "butt",
          borderDash: [],
          borderDashOffset: 0.0,
          borderJoinStyle: "miter",
          pointBorderColor: "rgba(75,192,192,1)",
          pointBackgroundColor: "#fff",
          pointBorderWidth: 1,
          pointHoverRadius: 5,
          pointHoverBackgroundColor: "rgba(75,192,192,1)",
          pointHoverBorderColor: "rgba(220,220,220,1)",
          pointHoverBorderWidth: 2,
          pointRadius: 1,
          pointHitRadius: 10,
          showLine: true,
          data: ajaxResponse
        }
      ]
    };

    return (
      <RowContainer>
        <InnerRow>
          <RowItem>
            <Title>{title}</Title>
          </RowItem>
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
            <RowItem widthPercent={"50%"}>
              <Scatter data={data} options={{ maintainAspectRatio: false }} />
            </RowItem>
            <RowItem widthPercent={"50%"}>
              <Scatter data={data} options={{ maintainAspectRatio: false }} />
            </RowItem>
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
