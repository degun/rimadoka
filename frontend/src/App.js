import { useState, useEffect } from "react";
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import axios from "axios";

import { HOST, vowels, accentedVowels } from "./constants";
import "./App.sass";

function App() {

  const [search, setSearch] = useState("");
  const [word, setWord] = useState("");
  const [accentIndex, setAccentIndex] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [rhymes, setRhymes] = useState([]);
  // const [selectedWord, setSelectedWord] = useState("");

  useEffect(() => {
    if(search)
    axios.get(`${HOST}/rima/browse/?search=${search}`).then(response => {
      setSuggestions(response.data.flatMap(({ fields }) => {
        return {
          label: fields.word,
          value: fields.index,
        }
      }));
    });
  }, [search]);

  useEffect(() => {
    if(word){
      // setSelectedWord(word);
    }else{
      setAccentIndex(null);
      setRhymes([]);
    }
  }, [word]);

  useEffect(() => {
    if(accentIndex !== null && word){
      const tail = word.substr(accentIndex);
      axios.get(`${HOST}/rima/rhymes/?word=${word}&tail=${tail}`).then(response => {
        setRhymes(response.data);
      })
    }
  }, [accentIndex, word]);

  // useEffect(() => {
  //   axios.get(`${FJALORTHI_API}${selectedWord}`).then(response => {
  //     console.log(response.data);
  //   })
  // }, [selectedWord]);

  function calculateAccent(letter, index){
    if(vowels.includes(letter) ){
      setAccentIndex(index === accentIndex ? null : index);
    }
  }

  const fullRhymes = rhymes.filter(({ type }) => type === "r");
  const asonances = rhymes.filter(({ type }) => type === "a");
  const consonances = rhymes.filter(({ type }) => type === "c");

  const myTheme = createTheme({
    palette:{
      mode: 'dark',
    }
});

  return (
    <div className="App">
      <header className="header">
      <ThemeProvider theme={myTheme}>
        <Autocomplete
          value={search}
          onInputChange={(_,val) => setSearch(val)}
          onChange={(_,val) => {setWord(val?.label ?? ''); setAccentIndex(val?.label ? (val.label.length - val.value - 1) : null)}}
          onKeyUp={({target}) => setWord(target.value)}
          selectOnFocus
          clearOnBlur
          handleHomeEndKeys
          autoComplete
          freeSolo
          size="small"
          id="free-solo-with-text-demo"
          options={suggestions.filter((value, index, self) => self.indexOf(value) === index)}
          sx={{ width: 300 }}
          renderInput={(params) => (
            <TextField {...params} label="Kërko fjalë" />
          )}
        />
        </ThemeProvider>
        <div className="word">
          {word && [...word].map((letter, index) => <span key={`letter-${index}`} className={index === accentIndex ? "accented" : undefined} onClick={() => calculateAccent(letter, index)}>{index === accentIndex ? accentedVowels[vowels.indexOf(letter)] : letter}</span>)}
        </div>
      </header>
      <main>
        <div className="rhymes">
            {fullRhymes.length ? <div className="section">
              <h3>Rima ({fullRhymes.length})</h3>
              {fullRhymes.map(({word, index}, i) => <span>
                <span className="word" onClick={() => {setWord(word); setAccentIndex(word.length - index - 1)}} key={i}>
                  <span>{word.substr(0,word.length - index - 1)}</span>
                  <span className="marked">{word.substr(word.length - index - 1)}</span>
                </span>
                {i < fullRhymes.length - 1 && <span className="separator">, </span>}
              </span>)}
            </div> : null}
            {asonances.length ? <div className="section">
              <h3>Asonanca ({asonances.length})</h3>
              {asonances.map(({word: w, index}, i) => <span>
                <span className="word" onClick={() => {setWord(w); setAccentIndex(w.length - index - 1)}} key={i}>
                  {[...w].map((letter, j) => <span key={`consonance-${word}-${j}`} className={j >= w.length - index - 1 && vowels.includes(letter) ? "marked" : ""}>{letter}</span>)}
                </span>
                {i < asonances.length - 1 && <span className="separator">, </span>}
              </span>)}
            </div> : null}
            {consonances.length ? <div className="section">
              <h3>Konsonanca ({consonances.length})</h3>
              {consonances.map(({word: w, index}, i) => <span>
                <span className="word" onClick={() => {setWord(w); setAccentIndex(w.length - index - 1)}} key={i}>
                  {[...w].map((letter, j) => <span key={`consonance-${word}-${j}`} className={j >= w.length - index - 1 && !vowels.includes(letter) ? "marked" : ""}>{letter}</span>)}
                </span>
                {i < consonances.length - 1 && <span className="separator">, </span>}
              </span>)}
            </div> : null}
        </div>
        <div className="definition">
        </div>
      </main>
    </div>
  );
}

export default App;
