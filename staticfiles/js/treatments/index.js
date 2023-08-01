window.addEventListener('DOMContentLoaded', (event) => {

  const batchItemTemplate = [
    '<tr class="item filtered" data-source="{{ source }}" data-filter-type="{{ status }}" data-filter-type2="{{ promo }}">',
    '<td>',
    '<label class="switch">',
    '<span class="toggle-label-title">Sélectionner le batch</span>',
    '<input type="checkbox" class="select-batch">',
    '<span class="slider round"></span>',
    '</label>',
    '</td>',
    '<td>{{ promo }}</td>',
    '<td>{{ name }}</td>',
    '<td>{{ param1 }}</td>',
    '<td>{{ status }}</td>',
    '<td><a href="{{ url }}" class="play-btn" aria-label="Lancer le batch de traitement"><svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="16px" height="16px" viewBox="0 0 1280.000000 1130.000000" preserveAspectRatio="xMidYMid meet"><g transform="translate(0.000000,1130.000000) scale(0.100000,-0.100000)" fill="#000000" stroke="none"><path d="M6223 11238 c-13 -6 -36 -32 -52 -57 -16 -25 -510 -878 -1099 -1896 -1218 -2107 -2695 -4661 -4078 -7050 -766 -1325 -949 -1648 -952 -1681 -3 -35 1 -47 26 -75 l30 -34 6172 0 6172 0 29 33 c52 58 46 78 -104 337 -74 127 -492 849 -929 1605 -2253 3896 -5066 8758 -5078 8776 -29 47 -90 65 -137 42z"/></g></svg></i></a></td>',
    '<td><span></span></td>',
    '</tr>'
  ];

  const batchItemTemplateAcheve = [
    '<tr class="item filtered" data-source="{{ source }}" data-filter-type="{{ status }}" data-filter-type2="{{ promo }}">',
    '<td>',
    '<label class="switch">',
    '<span class="toggle-label-title">Sélectionner le batch</span>',
    '<input type="checkbox" class="select-batch">',
    '<span class="slider round"></span>',
    '</label>',
    '</td>',
    '<td>{{ promo }}</td>',
    '<td>{{ name }}</td>',
    '<td>{{ param1 }}</td>',
    '<td>{{ status }}</td>',
    '<td><a href="{{ url }}" class="play-btn" aria-label="Lancer le batch de traitement"><svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="16px" height="16px" viewBox="0 0 1280.000000 1130.000000" preserveAspectRatio="xMidYMid meet"><g transform="translate(0.000000,1130.000000) scale(0.100000,-0.100000)" fill="#000000" stroke="none"><path d="M6223 11238 c-13 -6 -36 -32 -52 -57 -16 -25 -510 -878 -1099 -1896 -1218 -2107 -2695 -4661 -4078 -7050 -766 -1325 -949 -1648 -952 -1681 -3 -35 1 -47 26 -75 l30 -34 6172 0 6172 0 29 33 c52 58 46 78 -104 337 -74 127 -492 849 -929 1605 -2253 3896 -5066 8758 -5078 8776 -29 47 -90 65 -137 42z"/></g></svg></a></td>',
    '<td><a target="_blank" href="{{ results }}" data-report="{{ resultsReport }}" class="results-btn" aria-label="Voir resultats">Voir résultats</a></td>',
    '</tr>'
  ];

  const listeHtml = document.querySelector('.mon-container-list');

  let html = '';

  for (var i = 0; i < batchs.length; i++) {
    let url = "/" + batchs[i].endpoint + "/" + batchs[i].task_id + "/" + batchs[i].annee_universitaire;
    let libelleAnnee = batchs[i].annee_universitaire.split('_').join(' - 20').replace('-', '').trim();
    let showResultsReport = batchs[i].show_results_report;
    let rslt = '';

    if (showResultsReport) {
      rslt = "/" + batchs[i].endpoint + "_rapport_resultats/" + batchs[i].annee_universitaire;
    }

    if (batchs[i].status === 'Terminé') {
      html += `${batchItemTemplateAcheve.join('')
        .replace('{{ name }}', batchs[i].nom)
        .replaceAll('{{ promo }}', libelleAnnee)
        .replaceAll('{{ status }}', batchs[i].status)
        .replaceAll('{{ param1 }}', '')
        .replace('{{ url }}', url)
        .replace('{{ source }}', batchs[i].endpoint)
        .replace('{{ resultsReport }}', showResultsReport)
        .replace('{{ results }}', rslt)
        }`;
    } else {
      html += `${batchItemTemplate.join('')
        .replace('{{ name }}', batchs[i].nom)
        .replaceAll('{{ promo }}', libelleAnnee)
        .replaceAll('{{ status }}', batchs[i].status)
        .replaceAll('{{ param1 }}', '')
        .replace('{{ url }}', url)
        .replace('{{ source }}', batchs[i].endpoint)
        }`;
    }
  }

  document.getElementById('maListeHtml').innerHTML = html;

  const checkBoxesStatus = document.querySelectorAll('[name=status]');
  const checkBoxesProm = document.querySelectorAll('[name=prom]');
  const items = document.querySelectorAll('.item');
  const filterBtn = document.querySelector('.filter-btn');

  const toggleSwitchs = document.querySelectorAll('.select-batch');

  const playSelectionBtn = document.querySelector('.play-selection a');

  filterBtn.addEventListener('click', function (e) {

    const checkedStatus = Array.from(checkBoxesStatus).filter(filter => filter.checked).map(filter => filter.value);
    const checkedProm = Array.from(checkBoxesProm).filter(filter => filter.checked).map(filter => filter.value);
    const filteredItems = [];
    const finalFilteredItems = [];

    sessionStorage.setItem("etat_filters_appariements", checkedStatus);
    sessionStorage.setItem("annee_filters_appariements", checkedProm);

    items.forEach(item => {
      item.classList.remove('filtered');
      let itemType = item.getAttribute('data-filter-type');
      applyFilters(filteredItems, itemType, checkedStatus, item);
    })
    console.log('1', filteredItems);

    filteredItems.forEach(item => {
      let itemType2 = item.getAttribute('data-filter-type2');
      applyFilters(finalFilteredItems, itemType2, checkedProm, item)
    })
    console.log('2', finalFilteredItems);

    finalFilteredItems.forEach(item => {
      item.classList.add('filtered');
    })
  })

  function applyFilters(resultsArray, filterType, selectedFilters, item) {
    if (selectedFilters.indexOf(filterType) >= 0 || selectedFilters.length == 0) {
      resultsArray.push(item);
    }
  }

  let yearsSelection = [];
  let urlsSelection = [];

  toggleSwitchs.forEach(item => {
    item.addEventListener('click', function (e) {
      let playBtn = this.parentElement.parentElement.parentElement.querySelector('.play-btn');
      let year = playBtn.href.split('/').splice(-1).join();
      let validYearsSelection = true;
      let symbol = "-";
      let urlToTransform = playBtn.href.split('/').splice(5, 1).join();

      // si on met le toggle à faux
      if (!this.checked && this.parentElement.classList.contains('on')) {
        this.parentElement.classList.remove("on");

        if (playBtn) {
          // on enleve l'annee du tableau des annees selectionnees
          if (year) {
            let indexOfYear = yearsSelection.indexOf(year)
            if (indexOfYear > -1) {
              yearsSelection.splice(indexOfYear, 1);
            };
          }
          // on enlève l'url du tableau des urls selectionnees
          let indexOfUrl = urlsSelection.indexOf(urlToTransform)
          if (indexOfUrl > -1) {
            urlsSelection.splice(indexOfUrl, 1);
          };
        }
      } else {
        this.parentElement.classList.add("on");

        if (playBtn) {
          if (year) {
            yearsSelection.push(year);
          }
        }
        urlsSelection.push(urlToTransform)
      }

      //on regarde si toutes les annnees selectionnees sont les mêmes
      console.log(yearsSelection);
      validYearsSelection = yearsSelection.every(e => e === yearsSelection[0])

      // si ce n'est pas le cas, on enleve le href du bouton
      if (!validYearsSelection) {
        if (!playSelectionBtn.classList.contains('disabled')) {
          playSelectionBtn.classList.add('disabled');
        }
        playSelectionBtn.removeAttribute('href');

        // si c'est le cas on construit l'url du batch multiple
      } else {
        if (playSelectionBtn.classList.contains('disabled')) {
          playSelectionBtn.classList.remove('disabled');
        }

        let finalUrl = ''
        for (let i = 0; i < urlsSelection.length; i++) {
          if (i === urlsSelection.length - 1) {
            symbol = "";
          }
          finalUrl += urlsSelection[i] + symbol
        }

        playSelectionBtn.href = "/bulk_batch/appariements/" + finalUrl;
      }
    })
  })

  let etatSessionStorage = sessionStorage.getItem("etat_filters_appariements");
  let anneeSessionStorage = sessionStorage.getItem("annee_filters_appariements");

  if (etatSessionStorage || anneeSessionStorage) {
    let etatArray = etatSessionStorage.split(',');
    let anneeArray = anneeSessionStorage.split(',');

    if (anneeArray.length > 0 && anneeArray[0]) {
      let parentFilterYear = document.querySelector('.filters-fieldset details:first-of-type');
      parentFilterYear.setAttribute('open', '');

      checkBoxesProm.forEach(e => {
        if (anneeArray.indexOf(e.value) >= 0) {
          if (!e.checked) {
            e.click();
          };
        }
      })
    }

    if (etatArray.length > 0 && etatArray[0]) {
      let parentFilterYear = document.querySelector('.filters-fieldset details:nth-of-type(2)');
      parentFilterYear.setAttribute('open', '');

      checkBoxesStatus.forEach(e => {
        if (etatArray.indexOf(e.value) >= 0) {
          if (!e.checked) {
            e.click();
          }
        }
      })
    }

    filterBtn.click();
  }

})


