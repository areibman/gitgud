import * as React from "react";
import styled, { injectGlobal } from "styled-components";
import { DataContainer } from "./components/Hackathon/DataContainer";
import { SearchComponent } from "./components/Hackathon/SearchComponent";
import { champData } from "./assets/champions/champion.output.js";
import axios from "axios";

injectGlobal`
  body{
    margin: unset;
    font-family: Arial;
  }
  & * {
    box-sizing: border-box;
    outline: none;
  }
`;

axios.defaults.baseURL = "http://localhost:5000/";

const Sandbox = styled.div`
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  background-color: #c5f1fa;
  cursor: ${props =>
    props.itIsTeemoTime
      ? "url(" +
        require("./assets/champions/champion/TinyTeemo.png") +
        "), auto !important;"
      : "initial"};
`;

const SearchInformation = styled.div`
  display: flex;
  align-items: center;
  padding: 0px 15px;
  min-height: 40px;
  border-bottom: 1px solid #008cba;
  background-color: #c5f1fa;
  img {
    width: 32px;
    height: 32px;
    margin-right: 5px;
  }
`;

const InfoComponent = styled.div`
  margin-right: 10px;
`;

const HiddenWrapper = styled.span`
  width: 18px;
  height: 18px;
  position: absolute;
  top: 0;
  right: 0;

  :hover {
    img {
      visibility: visible;
    }
  }
`;

const DarkLordTeemo = styled.img`
  visibility: hidden;
`;

const ErrorText = styled.span`
  font-size: 18px;
`;

class App extends React.PureComponent {
  state = {
    hasActiveSearch: false,
    searchValue: "",
    searchRegion: "",
    searchRegionKey: "",
    searchChampion: "",
    searchChampionKey: "",
    itIsTeemoTime: false,
    requestedData: []
  };

  componentDidUpdate(prevProps, prevState) {
    if (this.state.searchChampion) {
      const selectedChampImage = champData.filter(champ => {
        if (champ.name === this.state.searchChampion) {
          return champ.image;
        }
        return "";
      });
      const image =
        selectedChampImage.length !== 0 ? selectedChampImage[0].image : "";
      document.getElementById(
        "champImg"
      ).src = require("./assets/champions/champion/" + image);
    }
  }

  search = async (
    searchValue,
    searchRegion,
    searchRegionKey,
    searchChampion,
    searchChampionKey
  ) => {
    let requestedData;
    this.setState({ loading: true });
    await axios
      .get("/firstRecallBuy", {
        params: {
          region: searchRegionKey,
          summonerName: searchValue,
          champion: searchChampionKey
        }
      })
      .then(response => {
        console.log("success", response);
        requestedData = response.data;
      })
      .catch(error => {
        console.log("error", error);
      })
      .then(() => {
        console.log("theend");
      });

    this.setState({
      hasActiveSearch: true,
      searchValue,
      searchRegion,
      searchRegionKey,
      searchChampion,
      searchChampionKey,
      requestedData
    });
  };

  itsTeemoTime = () => {
    this.setState({ itIsTeemoTime: !this.state.itIsTeemoTime });
  };

  render() {
    const hasActiveSearch =
      this.state.searchValue &&
      this.state.searchRegionKey &&
      this.state.searchChampionKey;

    return (
      <Sandbox id="sandbox" itIsTeemoTime={this.state.itIsTeemoTime}>
        <HiddenWrapper>
          <DarkLordTeemo
            src={require("./assets/champions/champion/TinyTeemo.png")}
            onClick={this.itsTeemoTime}
          />
        </HiddenWrapper>
        <SearchComponent search={this.search} champData={champData} />
        {hasActiveSearch ? (
          <React.Fragment>
            <SearchInformation>
              <InfoComponent>
                Summoner: {this.state.searchValue} |
              </InfoComponent>
              <InfoComponent>{this.state.searchRegion} | </InfoComponent>
              <InfoComponent>{this.state.searchChampion}</InfoComponent>
              <img id="champImg" alt={this.state.searchChampion} />
            </SearchInformation>
          </React.Fragment>
        ) : (
          <ErrorText>Please select a summoner, champion, and region.</ErrorText>
        )}
        <DataContainer
          showSearch={hasActiveSearch}
          requestedData={this.state.requestedData}
        />
      </Sandbox>
    );
  }
}

export default App;
