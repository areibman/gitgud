import * as React from "react";
import styled from "styled-components";
import { darken } from "polished";
import Select from "react-select";

const SearchContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  min-height: 125px;
  background-color: #c5f1fa;
  border-bottom: 1px solid #008cba;
  padding: 0px 15px;
`;

const ProjectName = styled.span`
  width: 18%;
  font-size: 45px;
  font-weight: bold;
  color: white;
  -webkit-text-stroke: 1px #008cba;
`;

const InputsColumn = styled.div`
  display: flex;
  flex-direction: column
  justify-content: space-between;
  width: 58%;
  height: 80px;
`;

const SelectRow = styled.div`
  display: flex;
  justify-content: space-between;
  & > * {
    width: 48%;
  }
`;

const SearchInput = styled.input.attrs({
  placeholder: "Summoner Name. Ex. ImaAsheHole"
})`
  height: 36px;
  border-radius: 4px;
  outline: none;
  border: 1px solid gainsboro;
  padding-left: 4px;
`;

const SearchButton = styled.button.attrs({
  type: "button"
})`
  width: 18%;
  height: 50%;
  font-size: 18px;
  font-weight: bold;
  color: white;
  background-color: #008cba;
  border-radius: 4px;
  cursor: pointer;
  :hover {
    background-color: ${darken(0.1, "#008cba")};
  }
  transition: all 0.3s ease;
`;

export class SearchComponent extends React.PureComponent {
  state = {
    searchValue: "",
    selectedRegion: null,
    selectedChampion: null
  };

  valueChange = e => {
    this.setState({ searchValue: e.target.value });
  };

  search = () => {
    this.props.search(
      this.state.searchValue,
      (this.state.selectedRegion || { value: "" }).value,
      (this.state.selectedChampion || { label: "" }).label,
      (this.state.selectedChampion || { value: "" }).value
    );
  };

  handleRegionChange = selectedOption => {
    this.setState({ selectedRegion: selectedOption });
  };

  handleChampionChange = selectedOption => {
    this.setState({ selectedChampion: selectedOption });
  };

  render() {
    const champions = this.props.champData.map(champ => {
      return { value: champ.championId, label: champ.name };
    });
    const regions = [
      { value: "EUNE", label: "EUNE" },
      { value: "EUW", label: "EUW" },
      { value: "NA", label: "NA" },
      { value: "BR", label: "BR" },
      { value: "LAN", label: "LAN" },
      { value: "LAS", label: "LAS" },
      { value: "OCE", label: "OCE" },
      { value: "KR", label: "KR" },
      { value: "RU", label: "RU" },
      { value: "TR", label: "TR" },
      { value: "JP", label: "JP" }
    ];
    return (
      <SearchContainer>
        <ProjectName> GitGud </ProjectName>
        <InputsColumn>
          <SearchInput
            value={this.state.searchValue}
            onChange={this.valueChange}
          />
          <SelectRow>
            <Select
              options={regions}
              onChange={this.handleRegionChange}
              placeholder="Select Region"
            />
            <Select
              options={champions}
              onChange={this.handleChampionChange}
              placeholder="Select Champion"
            />
          </SelectRow>
        </InputsColumn>
        <SearchButton onClick={this.search}> Search </SearchButton>
      </SearchContainer>
    );
  }
}
