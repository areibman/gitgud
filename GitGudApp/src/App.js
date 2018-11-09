import * as React from "react";
import { transparentize } from "polished";
import styled, { injectGlobal, keyframes } from "styled-components";
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
  ${props =>
    props.loading
      ? "visibility: hidden; min-height: 0px; height: 0px;"
      : "visibility: visible;"};
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

const LoadingDiv = styled.div`
  position: absolute;
  top: 175px;
  left: 0;
  height: calc(${window.innerHeight}px - 195px);
  width: calc(100% - 20px);
  background-color: ${transparentize(0.2, "white")};
  border-radius: 4px;
  margin: 10px;
  overflow: hidden;
`;

const LoadingDivAgain = styled.div`
  position: absolute;
  top: 175px;
  font-size: 48px;
  font-weight: bold;
  text-align: center;
  width: calc(100% - 20px);
  border-radius: 4px;
  margin: 10px;
  color: white;
  -webkit-text-stroke: 1px #008cba;
  overflow: hidden;
`;

const teemoframes = keyframes`
  0% {
    margin: 15px;
  }
  25% {
    margin: calc(${window.innerHeight}px - 345px) 0 0 0;
  }
  50% {
    margin: calc(${window.innerHeight}px - 345px) 0 0 calc(100% - 128px);
  }
  75% {
    margin: 0 0 0 calc(100% - 128px);
  }
  100% {
    margin: 15px;
    transform:rotateZ(1800deg);
  }
`;

const TeemoFace = styled.img`
  position: relative;
  height: 128px;
  width: 128px;
  margin: 0;
  padding: 3vmin;
  overflow: hidden;
  animation-name: ${teemoframes};
  animation-duration: 12s;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  animation-delay: 0s;
  background-image: ${"url(" +
    require("./assets/champions/champion/Teemo.png") +
    ");"};
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
    requestedData: [],
    loading: false
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
    await this.setState({ loading: true });
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
      loading: false,
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
        {hasActiveSearch && (
          <React.Fragment>
            <SearchInformation loading={this.state.loading}>
              <InfoComponent>
                Summoner: {this.state.searchValue} |
              </InfoComponent>
              <InfoComponent>{this.state.searchRegion} | </InfoComponent>
              <InfoComponent>{this.state.searchChampion}</InfoComponent>
              <img id="champImg" alt={this.state.searchChampion} />
            </SearchInformation>
          </React.Fragment>
        )}
        {this.state.loading && (
          <LoadingDiv>
            <LoadingDivAgain>Loading...</LoadingDivAgain>
            <TeemoFace />
          </LoadingDiv>
        )}
        <DataContainer
          showSearch={hasActiveSearch}
          loading={this.state.loading}
          requestedData={this.state.requestedData}
        />
      </Sandbox>
    );
  }
}

export default App;
