export const parseJson = json => {
  try {
    return JSON.parse(json);
  } catch (e) {
    console.error(e);
    return e;
  }
};

export const randomLog = val => Math.log(val) / 10000000000000;

export const customStyles = {
  option: provided => ({
    ...provided,
    background: "#92d4f6",
    color: "#fff",
    padding: 20
  }),
  control: provided => ({
    // none of react-select's styles are passed to <Control />
    ...provided,
    maxWidth: "50vw",
    margin: "auto",
    marginTop: "1rem",
    marginBottom: "2rem",
    border: 0
  }),
  menu: provided => ({
    ...provided,
    maxWidth: "50vw",
    margin: "auto",
    boxShaddow: 0,
    left: 0,
    right: 0
  })
};

export const options = [...Array(30).keys()].map((_, i) => ({
  label: `Season ${i + 1}`,
  value: i + 1
}));
