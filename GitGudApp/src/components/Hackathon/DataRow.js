import * as React from "react";
import styled from "styled-components";
import { Collapse } from "react-collapse";
import { Line, Scatter } from "react-chartjs-2";

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

const Chart = styled.div`
  min-width: 250px;
  min-height: 250px;
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

    var ajaxResponse = [{ x: 60, y: 0.005 }, { x: 80, y: 0.01 }, { x: 90, y: 0.02 }, { x: 111, y: 0.05 }, { x: 114, y: 0.50 }, { x: 160, y: 0.30 }, { x: 180, y: 0.10 }]

    const data = {
      datasets: [
        {
          label: "My First dataset",
          fill: true,
          lineTension: 0.1,
          backgroundColor: "rgba(75,192,192,0.4)",
          borderColor: "rgba(75,192,192,1)",
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
            <Chart>
              <Scatter data={data} />
            </Chart>
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
