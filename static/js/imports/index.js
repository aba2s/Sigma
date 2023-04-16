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
    '<td>{{ status }}</td>',
    '<td><a href="{{ url }}" class="play-btn" aria-label="Importer les données du batch"><svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="16px" height="16px" viewBox="0 0 1280.000000 1130.000000" preserveAspectRatio="xMidYMid meet"><g transform="translate(0.000000,1130.000000) scale(0.100000,-0.100000)" fill="#000000" stroke="none"><path d="M6223 11238 c-13 -6 -36 -32 -52 -57 -16 -25 -510 -878 -1099 -1896 -1218 -2107 -2695 -4661 -4078 -7050 -766 -1325 -949 -1648 -952 -1681 -3 -35 1 -47 26 -75 l30 -34 6172 0 6172 0 29 33 c52 58 46 78 -104 337 -74 127 -492 849 -929 1605 -2253 3896 -5066 8758 -5078 8776 -29 47 -90 65 -137 42z"/></g></svg></a></td>',
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
    '<td>{{ status }}</td>',
    '<td><a href="{{ url }}" class="play-btn popin-cancel-replace" aria-label="Importer les données du batch"><svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="16px" height="16px" viewBox="0 0 1280.000000 1130.000000" preserveAspectRatio="xMidYMid meet"><g transform="translate(0.000000,1130.000000) scale(0.100000,-0.100000)" fill="#000000" stroke="none"><path d="M6223 11238 c-13 -6 -36 -32 -52 -57 -16 -25 -510 -878 -1099 -1896 -1218 -2107 -2695 -4661 -4078 -7050 -766 -1325 -949 -1648 -952 -1681 -3 -35 1 -47 26 -75 l30 -34 6172 0 6172 0 29 33 c52 58 46 78 -104 337 -74 127 -492 849 -929 1605 -2253 3896 -5066 8758 -5078 8776 -29 47 -90 65 -137 42z"/></g></svg></a><a href="{{ stats }}" class="stats-btn" aria-label="View Stats"><svg xmlns="http://www.w3.org/2000/svg" height="33" viewBox="0 96 960 960" width="33"><path d="M279.915 637.462q8.7 0 15.124-6.338 6.423-6.339 6.423-15.039t-6.338-15.124q-6.339-6.423-15.039-6.423t-15.124 6.338q-6.423 6.339-6.423 15.039t6.338 15.124q6.339 6.423 15.039 6.423Zm0-160q8.7 0 15.124-6.338 6.423-6.339 6.423-15.039t-6.338-15.124q-6.339-6.423-15.039-6.423t-15.124 6.338q-6.423 6.339-6.423 15.039t6.338 15.124q6.339 6.423 15.039 6.423Zm84.7 153.923H700v-30.77H364.615v30.77Zm0-160H700v-30.77H364.615v30.77Zm0 424.615v-80H175.384q-23.057 0-39.221-16.163Q120 783.673 120 760.616V311.384q0-23.057 16.163-39.221Q152.327 256 175.384 256h609.232q23.057 0 39.221 16.163Q840 288.327 840 311.384v449.232q0 23.057-16.163 39.221Q807.673 816 784.616 816H595.385v80h-230.77ZM175.384 785.231h609.232q9.23 0 16.923-7.692 7.692-7.693 7.692-16.923V311.384q0-9.23-7.692-16.923-7.693-7.692-16.923-7.692H175.384q-9.23 0-16.923 7.692-7.692 7.693-7.692 16.923v449.232q0 9.23 7.692 16.923 7.693 7.692 16.923 7.692Zm-24.615 0V286.769 785.231Z"/></svg></a></td>',
    '</tr>'
  ];

  const listeHtml = document.querySelector('.mon-container-list');

  let html = '';

  for (var i = 0; i < batchs.length; i++) {
    let url = "/" + batchs[i].endpoint + "/" + batchs[i].task_id + "/" + batchs[i].annee_universitaire;
    if (batchs[i].status === 'Terminé') {
      let urlStat = "/" + batchs[i].endpoint + "_stats_popin/" + batchs[i].annee_universitaire;
      html += `${batchItemTemplateAcheve.join('')
        .replace('{{ stats }}', urlStat)
        .replace('{{ name }}', batchs[i].nom)
        .replaceAll('{{ promo }}', batchs[i].annee_universitaire_lb)
        .replaceAll('{{ status }}', batchs[i].status)
        .replace('{{ url }}', url)
        .replace('{{ source }}', batchs[i].endpoint)
        }`;
    } else {
      html += `${batchItemTemplate.join('')
        .replace('{{ name }}', batchs[i].nom)
        .replaceAll('{{ promo }}', batchs[i].annee_universitaire_lb)
        .replaceAll('{{ status }}', batchs[i].status)
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

  const statsBtns = document.querySelectorAll('.stats-btn');
  const popinStats = document.querySelector('.stats-popin');
  const popinClose = document.querySelector('.popin-close');

  const replaceBtns = document.querySelectorAll('.popin-cancel-replace');
  const popinReplace = document.querySelector('.cancel-and-replace-popin');
  const cancelBtn = document.querySelector('.btn-cancel');
  const replaceBatchBtn = document.querySelector('.btn-replace');
  const popinReplaceClose = document.querySelector('.popin-cancel-replace-close');

  const toggleSwitchs = document.querySelectorAll('.select-batch');

  const playSelectionBtn = document.querySelector('.play-selection a');

  const nbLignes = document.querySelector('.nb-lignes');
  const nbColonnes = document.querySelector('.nb-colonnes');
  const missingRate = document.querySelector('.missing-rate');
  const perfectDuplicates = document.querySelector('.perfect-duplicates');
  const diffIdDuplicates = document.querySelector('.diff-id-duplicates');
  const sameIdDuplicates = document.querySelector('.same-id-duplicates');
  const aPopin = document.querySelector('.export a');

  statsBtns.forEach(item => {
    item.addEventListener('click', function (e) {
      let urlToCall = this.href
      let urlToCallReport = urlToCall.replace('_stats_popin', '_export_stats_popin');
      aPopin.href = urlToCallReport;
      e.preventDefault();
      fetch(urlToCall)
        .then(function (response) {
          return response.json();
        })
        .then(function (data) {
          // console.log('stats', data)
          nbLignes.innerText = data.nb_lignes;
          nbColonnes.innerText = data.nb_colonnes;
          missingRate.innerText = data.taux_donnees_manquantes;
          perfectDuplicates.innerText = data.nb_doublons_parfaits;
          diffIdDuplicates.innerText = data.nb_doub_diff_id;
          sameIdDuplicates.innerText = data.nb_doub_same_id;
          popinStats.style.display = "block";
        })
        .catch(error => console.error(error));
    })
  })

  popinClose.addEventListener('click', function () {
    popinStats.style.display = "none";
  })

  window.onclick = function (event) {
    if (event.target == popinStats) {
      popinStats.style.display = "none";
    }
    if (event.target == popinReplace) {
      popinReplace.style.display = "none";
    }
  }

  replaceBtns.forEach(item => {
    item.addEventListener('click', function (e) {
      e.preventDefault();
      let bacthToActivateHref = this.href;
      let urlsParts = bacthToActivateHref.split('/');
      let source = urlsParts[3] + '_annule_et_remplace';
      let finalUrl = bacthToActivateHref.replace(urlsParts[3], source);
      popinReplace.style.display = "block";
      replaceBatchBtn.href = finalUrl;
    })
  })

  popinReplaceClose.addEventListener('click', function () {
    popinReplace.style.display = "none";
  })

  cancelBtn.addEventListener('click', function () {
    popinReplace.style.display = "none";
  })

  filterBtn.addEventListener('click', function (e) {

    const checkedStatus = Array.from(checkBoxesStatus).filter(filter => filter.checked).map(filter => filter.value);
    const checkedProm = Array.from(checkBoxesProm).filter(filter => filter.checked).map(filter => filter.value);
    const filteredItems = [];
    const finalFilteredItems = [];

    sessionStorage.setItem("etat_filters", checkedStatus);
    sessionStorage.setItem("annee_filters", checkedProm);

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

  playSelectionBtn.addEventListener('click', function (e) {
    e.preventDefault()
    const result = [];
    const link = this
    toggleSwitchs.forEach(item => {
      let playBtn = item.parentElement.parentElement.parentElement.querySelector('.play-btn');
      if (item.checked) {
        if (playBtn) {
          result.push(playBtn);
        }
      }
    })
    console.log('result', result);
    if (result.length > 0) {
      let urlToCall = "/bulk_batch/";
      let includeCompletedBatch = [];

      for (let i = 0; i < result.length; i++) {
        let symbol = "-";
        if (i === result.length - 1) {
          symbol = "";
        }
        if ([...result[i].classList].includes('popin-cancel-replace')) {
          includeCompletedBatch.push(result[i])
        };

        let urlToTransform = result[i].href.split('/').splice(4,1).join();
      
        urlToCall +=  urlToTransform + symbol;
        link.href = urlToCall;
      }
      if (includeCompletedBatch.length > 0) {
        popinReplace.style.display = "block";
        const popinReplaceBtn = popinReplace.querySelector('.btn-replace')
        popinReplaceBtn.href = urlToCall;
      } else {
        location.href = link.href
      }
    }
    
    
  })

  let etatSessionStorage = sessionStorage.getItem("etat_filters");
  let anneeSessionStorage = sessionStorage.getItem("annee_filters");

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
          };
        }
      })
    }
    filterBtn.click();
  }

})


