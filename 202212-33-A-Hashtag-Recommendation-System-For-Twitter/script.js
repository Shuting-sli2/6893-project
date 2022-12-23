const defaultLimit = 20;

// setup controls
const satInput = document.querySelector('#sat');
const lumInput = document.querySelector('#lum');
const limitSelect = document.querySelector('#limit');
const shuffleSelect = document.querySelector('#shuffle');
const personalization = document.querySelector('#beta');
const options = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25];
options.forEach((val, i) => limitSelect.options[i] = new Option(val));
limitSelect.selectedIndex = defaultLimit - 1;
const bgSelect = document.querySelector('#bg');
bgSelect.selectedIndex = 0;
limitSelect.addEventListener('change', render);
bgSelect.addEventListener('change', render);
shuffleSelect.addEventListener('change', render);
personalization.addEventListener('change',render);

render();

function render(){
  let idx = 0;
  const limit = limitSelect.selectedIndex + 1;
  const bgColor = bgSelect.options[bgSelect.selectedIndex].value;
  const doShuffle = shuffleSelect.selectedIndex === 2;
  const accord2Volume = shuffleSelect.selectedIndex === 1;
  const beta = personalization.value;
  document.querySelector('#chart').innerHTML = '';

  var trend = [],
      user = [];

  const trendPromise = fetch('trend.json').then(res=>res.json())
  const userPromise = fetch('Twitter_Tweets.json').then(res=>res.json())

  Promise.all([trendPromise,userPromise]).then(values => {
    const data1 = values[0]
    const data2 = values[1]

    const data1_modified = data1.map(element => {
      element.weight = (1-beta) * Math.log(element.tweet_volume/23780)
      return element
    })
    trend = data1_modified

    const data2_modified = data2.map(element => {
      element.weight = (1-beta) * Math.log(element.tweet_volume/23780) + beta * (element.weight+5)
      return element
    })
    user = data2_modified

    trend.map(element =>{
      element['value'] = element['tweet_volume']
      delete element['tweet_volume']
    })

    user.map(element =>{
      element['value'] = element['tweet_volume']
      delete element['tweet_volume']
    })
    let final_data = trend.concat(user)
    final_data.sort((a,b) => {
      if(a.weight>b.weight) return -1;
      if(a.weight<b.weight) return 1;
      return 0;
    })

    final_data.map(element =>{
      const diameter = element.value>50000?element.value:50000
      element.diameter = diameter
      return element
    })

    console.log(final_data)

    if (accord2Volume){
      final_data.sort((a,b) => {
        if(a.value>b.value) return -1;
        if(a.value<b.value) return 1;
        return 0;
      })
    }

    if (doShuffle) {
      final_data = _.shuffle(final_data);  
    }
    

    var json = {'children':[]}
    json.children = final_data.slice(0,limit)

    
    const diameters = json.children.map(d => d.diameter);
    const min = Math.min.apply(null, diameters);
    const max = Math.max.apply(null, diameters);
    const total = json.children.length;
    
    document.body.style.backgroundColor = bgColor;  
      
    var diameter = 600,
        color = d3.scaleOrdinal(d3.schemeCategory20c);
    
    var bubble = d3.pack()
      .size([diameter, diameter])
      .padding(0);
    
    var tip = d3.tip()
      .attr('class', 'd3-tip-outer')
      .offset([-38, 0])
      .html((d, i) => {
        const item = json.children[i];
        const color = getColor(i, diameters.length);
        return `<div class="d3-tip" style="background-color: ${color}">${item.name} (${item.value})</div><div class="d3-stem" style="border-color: ${color} transparent transparent transparent"></div>`;
      })
    ;
      
    var margin = {
      left: 25,
      right: 25,
      top: 25,
      bottom: 25
    }
    
    var svg = d3.select('#chart').append('svg')
      .attr('viewBox','0 0 ' + (diameter + margin.right) + ' ' + diameter)
      .attr('width', (diameter + margin.right))
      .attr('height', diameter)
      .attr('class', 'chart-svg');
    
    var root = d3.hierarchy(json)
      .sum(function(d) { return d.diameter; });
      // .sort(function(a, b) { return b.value - a.value; });
    
    bubble(root);
    
    var node = svg.selectAll('.node')
      .data(root.children)
      .enter()
      .append('g').attr('class', 'node')
      .attr('transform', function(d) { return 'translate(' + d.x + ' ' + d.y + ')'; })
      .append('g').attr('class', 'graph');
    
    function onclick(){
      console.log('click')
    }

    node.append("circle")
      .on('click', function(d){
        var result = d.data.name.split('#').join('%23');
        window.open('https://twitter.com/search?q='+result);
      })
      .attr("r", function(d) { return d.r; })
      .style("fill", getItemColor)
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide);
    
    node.call(tip);
      
    node.append("text")
      .attr("dy", "0.2em")
      .style("text-anchor", "middle")
      .style('font-family', 'Roboto')
      .style('font-size', getFontSizeForItem)
      .text(getLabel)
      .style("fill", "#ffffff")
      .style('pointer-events', 'none');
    
    node.append("text")
      .attr("dy", "1.3em")
      .style("text-anchor", "middle")
      .style('font-family', 'Roboto')
      .style('font-weight', '100')
      .style('font-size', getFontSizeForItem)
      .text(getValueText)
      .style("fill", "#ffffff")
      .style('pointer-events', 'none');  
      
    function getItemColor(item) {
      return getColor(idx++, json.children.length);
    }
    function getColor(idx, total) {
      //const colorList = ['F05A24','EF4E4A','EE3F65','EC297B','E3236C','D91C5C','BC1E60','9E1F63','992271','952480','90278E','7A2A8F','652D90','502980','3B2671','262261','27286D','292D78','2A3384','2B388F','2A4F9F','2965AF','277CC0','2692D0','25A9E0'];
      const colorList = ['FF0000','EE082E','E40D52','D91074','CD1392','B816A2','9A18AF','7E1AA6','5B1EA0','44219A','342390','262589','28277E','272C7E','262B78','26326F','263066','263866','263760','263F60','243A57','243F57','243C51','244351','26454A']
      const colorLookup = [
        [0,4,10,18,24],
        [0,3,6,9,11,13,15,18,20,24],
        [0,3,4,6,7,9,11,13,14,15,17,18,20,22,24],
        [0,2,3,4,6,7,8,9,11,12,13,14,15,17,18,19,20,22,23,24],
        [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],
      ];  
      for (const idxList of colorLookup) {
        if (idxList.length >= total) {
          return '#' + colorList[idxList[idx]];
        }
      }
    }

    function getLabel(item) {
      if (item.data.diameter < max / 100) {
        return '';
      }
      return truncate(item.data.name);
    }
    function getValueText(item) {
      if (item.data.diameter < max / 100) {
        return '';
      }
      return item.data.value;
    }
    function truncate(label) {
      const max = 11;
      if (label.length > max) {
        label = label.slice(0, max) + '...';
      }
      return label;
    }
    function getFontSizeForItem(item) {
      return getFontSize(item.data.diameter, min, max, total);
    }
    function getFontSize(diameter, min, max, total) {
      const minPx = 6;
      const maxPx = 25;
      const pxRange = maxPx - minPx;
      const dataRange = max - min;
      const ratio = pxRange / dataRange;
      const size = Math.min(maxPx, Math.round(diameter * ratio) + minPx);
      return `${size}px`;
    }
  })
}