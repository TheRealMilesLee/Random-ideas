"use strict";
// a global variable to prevent race
let xhr = null;
// Get the element by using the id

function get_by_id(id)
{
  return document.getElementById(id);
}
// Get the element by using the name
function get_by_name(name)
{
  return document.getElementsByName(name);
}

get_by_name('openFileButton').addEventListener('click', () =>
{
  dialog.showOpenDialog({
    properties: ['openFile'],
    filters: [{ name: 'TeX Files', extensions: ['tex'] }]
  }).then(result =>
  {
    if (!result.canceled)
    {
      const filePath = result.filePaths[0];
      readFile(filePath);
    }
  }).catch(err =>
  {
    console.log(err);
  });
});

const fs = require('fs');

function readFile(filePath)
{
  fs.readFile(filePath, 'utf-8', (err, data) =>
  {
    if (err)
    {
      console.log(err);
      return;
    }
    displayFileContent(data);
  });
}

function displayFileContent(content)
{
  // Assume you have an element with ID 'editor' where you want to display the content
  document.getElementById('editor').innerText = content;
}

function renderTeX(content)
{
  const outputElement = get_by_id('output');
  outputElement.innerHTML = ''; // Clear previous content

  try
  {
    MathJax.texReset(); // Reset MathJax (optional)
    MathJax.typesetClear([outputElement]); // Clear previous MathJax typesetting (optional)

    MathJax.tex2chtmlPromise(content, { em: 16, ex: 8, display: true })
      .then((node) =>
      {
        outputElement.appendChild(node);
        MathJax.startup.document.clear(); // Clear MathJax startup document (optional)
        MathJax.startup.document.updateDocument(); // Update MathJax document (optional)
      })
      .catch((error) =>
      {
        console.log(error);
      });
  } catch (error)
  {
    console.log(error);
  }
}
