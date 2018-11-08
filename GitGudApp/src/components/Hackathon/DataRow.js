import * as React from "react";
import styled from "styled-components";
import { Collapse } from "react-collapse";
import { Line } from "react-chartjs-2";

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
    const data = {
      labels: ["January", "February", "March", "April", "May", "June", "July"],
      datasets: [
        {
          label: "My First dataset",
          fill: false,
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
          data: [65, 59, 80, 81, 56, 55, 40]
        },
        {
          label: "My First dataset",
          fill: false,
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
          data: [12, 70, 10, 91, 15, 35, 90]
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
              <Line data={data} />
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
