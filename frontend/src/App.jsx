import "./App.css";
import SearchBar from "./components/SearchBar";
import Table from "./components/Table";
import { useState, useEffect } from "react";

function App() {
  const [searchText, setSearchText] = useState("");
  const [selectedOption, setSelectedOption] = useState("name");
  const [tableData, setTableData] = useState([]);
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8080/jobs")
      .then((response) => response.json())
      .then((data) => {
        setData(data);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Erro ao buscar dados:", error);
        setIsLoading(false);
      });
  }, []);

  useEffect(() => {
    const newTableData = data.filter((job) =>
      job[selectedOption].toLowerCase().includes(searchText.toLowerCase())
    );
    setTableData(newTableData);
  }, [searchText, selectedOption, data]);

  function updateSearchText(newText) {
    setSearchText(newText);
    updateTableData();
  }

  function updateSelectedOption(newOption) {
    setSelectedOption(newOption);
    updateTableData();
  }

  return (
    <>
      <div></div>
      <header>
        <img className="logo-img" src="public/EmpregaDev.png" alt="logo" />{" "}
      </header>
      <SearchBar
        updateSearchText={updateSearchText}
        updateSelectedOption={updateSelectedOption}
      ></SearchBar>
      {isLoading ? 
      <div className="loading-container"><p>Carregando...</p></div>
      : <Table data={tableData}></Table>}
    </>
  );
}

export default App;
