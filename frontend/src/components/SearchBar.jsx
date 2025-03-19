export default function SearchBar({updateSearchText, updateSelectedOption}){
    return (<div className="search-bar-container">
        <input placeholder="Pesquisar..." className="search-bar" onChange={(event) => updateSearchText(event.target.value)}></input>
        <select name="search-options" className="search-options" onChange={(event) => updateSelectedOption(event.target.value)}>
            <option value="name">Nome</option>
            <option value="company">Empresa</option>
            <option value="website">Website</option>
        </select>
    </div>)
}