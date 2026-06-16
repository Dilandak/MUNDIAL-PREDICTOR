#!/usr/bin/env python3
"""
=============================================================
  🏆 MUNDIAL 2026 — PREDICTOR EN VIVO
=============================================================
Cada vez que corres este script:
  1. Descarga resultados reales de internet
  2. Muestra goleadores reales con minutos
  3. Usa los jugadores que ESTÁN jugando en el torneo
  4. Predice partidos pendientes con xG y probabilidades
=============================================================
"""

import requests, math
from collections import defaultdict
from datetime import datetime

DATA_URL = "https://raw.githubusercontent.com/openfootball/world-cup.json/master/2026/worldcup.json"

# ── Traducción de nombres ──────────────────────────────────
NOMBRES = {
    "Mexico":"México","South Africa":"Sudáfrica","South Korea":"Corea del Sur",
    "Czech Republic":"Rep. Checa","Canada":"Canadá","Bosnia & Herzegovina":"Bosnia y Herz.",
    "Qatar":"Qatar","Switzerland":"Suiza","Brazil":"Brasil","Morocco":"Marruecos",
    "Haiti":"Haití","Scotland":"Escocia","USA":"EE.UU.","Paraguay":"Paraguay",
    "Australia":"Australia","Turkey":"Turquía","Germany":"Alemania","Curaçao":"Curazao",
    "Ivory Coast":"Costa de Marfil","Ecuador":"Ecuador","Netherlands":"Países Bajos",
    "Japan":"Japón","Sweden":"Suecia","Tunisia":"Túnez","Belgium":"Bélgica",
    "Egypt":"Egipto","Iran":"Irán","New Zealand":"Nueva Zelanda","Spain":"España",
    "Cape Verde":"Cabo Verde","Saudi Arabia":"Arabia Saudita","Uruguay":"Uruguay",
    "France":"Francia","Senegal":"Senegal","Iraq":"Irak","Norway":"Noruega",
    "Argentina":"Argentina","Algeria":"Argelia","Austria":"Austria","Jordan":"Jordania",
    "Portugal":"Portugal","DR Congo":"Rep. D. del Congo","Uzbekistan":"Uzbekistán",
    "Colombia":"Colombia","England":"Inglaterra","Croatia":"Croacia","Ghana":"Ghana",
    "Panama":"Panamá",
}
def tr(n): return NOMBRES.get(n, n)

# ── Squads reales convocados al Mundial 2026 ──────────────
SQUADS = {
    "Francia": {
        "titulares": ["Mike Maignan","Jules Koundé","Dayot Upamecano","William Saliba","Theo Hernández","N'Golo Kanté","Aurélien Tchouaméni","Eduardo Camavinga","Ousmane Dembélé","Kylian Mbappé","Marcus Thuram"],
        "goleadores": ["Kylian Mbappé","Ousmane Dembélé","Marcus Thuram","Antoine Griezmann","Bradley Barcola"],
        "squad": ["Mike Maignan","Alphonse Areola","Guillaume Restes","Jules Koundé","Dayot Upamecano","William Saliba","Ibrahima Konaté","Theo Hernández","Lucas Hernández","Jonathan Clauss","Benjamin Pavard","Pau Cubarsí","N'Golo Kanté","Aurélien Tchouaméni","Eduardo Camavinga","Adrien Rabiot","Warren Zaïre-Emery","Kylian Mbappé","Ousmane Dembélé","Antoine Griezmann","Marcus Thuram","Randal Kolo Muani","Kingsley Coman","Bradley Barcola"],
    },
    "Argentina": {
        "titulares": ["Emiliano Martínez","Nahuel Molina","Cristian Romero","Lisandro Martínez","Nicolás Tagliafico","Rodrigo De Paul","Enzo Fernández","Alexis Mac Allister","Lionel Messi","Lautaro Martínez","Julián Álvarez"],
        "goleadores": ["Lionel Messi","Lautaro Martínez","Julián Álvarez","Paulo Dybala","Ángel Di María"],
        "squad": ["Emiliano Martínez","Gerónimo Rulli","Walter Benítez","Cristian Romero","Nicolás Otamendi","Lisandro Martínez","Nicolás Tagliafico","Nahuel Molina","Gonzalo Montiel","Germán Pezzella","Rodrigo De Paul","Enzo Fernández","Alexis Mac Allister","Leandro Paredes","Guido Rodríguez","Exequiel Palacios","Lionel Messi","Lautaro Martínez","Julián Álvarez","Ángel Di María","Paulo Dybala","Nicolás González","Thiago Almada"],
    },
    "España": {
        "titulares": ["Unai Simón","Dani Carvajal","Pau Cubarsí","Aymeric Laporte","Marc Cucurella","Rodri","Pedri","Fabián Ruiz","Lamine Yamal","Álvaro Morata","Nico Williams"],
        "goleadores": ["Lamine Yamal","Álvaro Morata","Nico Williams","Dani Olmo","Pedri"],
        "squad": ["Unai Simón","David Raya","Álex Remiro","Dani Carvajal","Aymeric Laporte","Robin Le Normand","Marc Cucurella","Alejandro Grimaldo","Nacho Fernández","Pau Cubarsí","Pedri","Gavi","Rodri","Fabián Ruiz","Mikel Merino","Dani Olmo","Lamine Yamal","Álvaro Morata","Nico Williams","Ferran Torres","Joselu","Bryan Zaragoza"],
    },
    "Brasil": {
        "titulares": ["Alisson","Danilo","Éder Militão","Marquinhos","Wendell","Casemiro","Bruno Guimarães","Lucas Paquetá","Raphinha","Vinicius Jr.","Rodrygo"],
        "goleadores": ["Vinicius Jr.","Rodrygo","Raphinha","Endrick","Gabriel Jesus"],
        "squad": ["Alisson","Ederson","Bento","Danilo","Éder Militão","Marquinhos","Gabriel Magalhães","Wendell","Alex Sandro","Guilherme Arana","Casemiro","Bruno Guimarães","Lucas Paquetá","Gerson","Andreas Pereira","Vinicius Jr.","Rodrygo","Endrick","Raphinha","Gabriel Martinelli","Gabriel Jesus","Savinho"],
    },
    "Alemania": {
        "titulares": ["Manuel Neuer","Joshua Kimmich","Nico Schlotterbeck","Antonio Rüdiger","David Raum","Toni Kroos","Ilkay Gündoğan","Florian Wirtz","Jamal Musiala","Kai Havertz","Leroy Sané"],
        "goleadores": ["Kai Havertz","Jamal Musiala","Florian Wirtz","Deniz Undav","Felix Nmecha","Nathaniel Brown"],
        "squad": ["Manuel Neuer","Marc-André ter Stegen","Oliver Baumann","Antonio Rüdiger","Nico Schlotterbeck","Jonathan Tah","David Raum","Joshua Kimmich","Matthias Ginter","Toni Kroos","Ilkay Gündoğan","Leon Goretzka","Felix Nmecha","Robert Andrich","Florian Wirtz","Kai Havertz","Jamal Musiala","Leroy Sané","Thomas Müller","Deniz Undav","Nathaniel Brown"],
    },
    "Inglaterra": {
        "titulares": ["Jordan Pickford","Kyle Walker","John Stones","Marc Guehi","Kieran Trippier","Trent Alexander-Arnold","Declan Rice","Jude Bellingham","Bukayo Saka","Harry Kane","Phil Foden"],
        "goleadores": ["Harry Kane","Jude Bellingham","Bukayo Saka","Phil Foden","Cole Palmer"],
        "squad": ["Jordan Pickford","Aaron Ramsdale","Dean Henderson","Kyle Walker","John Stones","Harry Maguire","Luke Shaw","Kieran Trippier","Marc Guehi","Ezri Konsa","Jude Bellingham","Declan Rice","Kobbie Mainoo","Trent Alexander-Arnold","Phil Foden","Conor Gallagher","Harry Kane","Marcus Rashford","Bukayo Saka","Eberechi Eze","Ollie Watkins","Cole Palmer"],
    },
    "Portugal": {
        "titulares": ["Diogo Costa","João Cancelo","Rúben Dias","Pepe","Nuno Mendes","João Palhinha","Bruno Fernandes","Bernardo Silva","Francisco Conceição","Cristiano Ronaldo","Rafael Leão"],
        "goleadores": ["Cristiano Ronaldo","Bruno Fernandes","Rafael Leão","Gonçalo Ramos","João Félix"],
        "squad": ["Diogo Costa","Rui Patrício","José Sá","Rúben Dias","Pepe","Nuno Mendes","João Cancelo","Diogo Dalot","António Silva","Bruno Fernandes","Bernardo Silva","João Palhinha","Rúben Neves","Vitinha","Matheus Nunes","Cristiano Ronaldo","Rafael Leão","Pedro Neto","Gonçalo Ramos","Francisco Conceição","João Félix"],
    },
    "Colombia": {
        "titulares": ["Camilo Vargas","Daniel Muñoz","Dávinson Sánchez","Yerry Mina","Johan Mojica","Richard Ríos","Jefferson Lerma","James Rodríguez","Luis Díaz","Falcao García","Jhon Córdoba"],
        "goleadores": ["Luis Díaz","James Rodríguez","Falcao García","Jhon Córdoba","Cucho Hernández"],
        "squad": ["Camilo Vargas","Kevin Mier","Álvaro Montero","Dávinson Sánchez","Yerry Mina","Daniel Muñoz","Johan Mojica","Carlos Cuesta","Jhon Lucumí","James Rodríguez","Mateus Uribe","Wilmar Barrios","Jefferson Lerma","Richard Ríos","Luis Díaz","Falcao García","Jhon Córdoba","Duván Zapata","Jorge Carrascal","Cucho Hernández"],
    },
    "Noruega": {
        "titulares": ["Ørjan Nyland","Stian Gregersen","Leo Østigård","Andreas Hanche-Olsen","Birger Meling","Fredrik Aursnes","Sander Berge","Martin Ødegaard","Antonio Nusa","Erling Haaland","Alexander Sørloth"],
        "goleadores": ["Erling Haaland","Alexander Sørloth","Martin Ødegaard","Antonio Nusa"],
        "squad": ["Ørjan Nyland","Jørgen Strand Larsen","Leo Østigård","Andreas Hanche-Olsen","Birger Meling","Elias Kristoffersen","Stian Gregersen","Martin Ødegaard","Sander Berge","Mathias Normann","Patrick Berg","Fredrik Aursnes","Erling Haaland","Alexander Sørloth","Mohamed Elyounoussi","Ola Solbakken","Antonio Nusa"],
    },
    "Uruguay": {
        "titulares": ["Sergio Rochet","Guillermo Varela","José María Giménez","Ronald Araújo","Mathías Olivera","Federico Valverde","Rodrigo Bentancur","Manuel Ugarte","Maxi Araújo","Darwin Núñez","Luis Suárez"],
        "goleadores": ["Darwin Núñez","Luis Suárez","Maxi Araújo","Federico Valverde","Facundo Torres"],
        "squad": ["Sergio Rochet","Fernando Muslera","Sebastián Sosa","José María Giménez","Ronald Araújo","Mathías Olivera","Nahitan Nández","Guillermo Varela","Federico Valverde","Rodrigo Bentancur","Manuel Ugarte","Lucas Torreira","Nicolás de la Cruz","Darwin Núñez","Luis Suárez","Maxi Araújo","Facundo Torres","Gastón Pereiro"],
    },
    "México": {
        "titulares": ["Guillermo Ochoa","Jorge Sánchez","César Montes","Johan Vásquez","Jesús Gallardo","Edson Álvarez","Carlos Rodríguez","Orbelín Pineda","Hirving Lozano","Raúl Jiménez","Julián Quiñones"],
        "goleadores": ["Raúl Jiménez","Julián Quiñones","Hirving Lozano","Henry Martín","Roberto Alvarado"],
        "squad": ["Guillermo Ochoa","Luis Malagón","Rodolfo Cota","César Montes","Johan Vásquez","Jesús Gallardo","Jorge Sánchez","Gerardo Arteaga","Edson Álvarez","Carlos Rodríguez","Luis Romo","Erick Gutiérrez","Orbelín Pineda","Hirving Lozano","Raúl Jiménez","Julián Quiñones","Henry Martín","Roberto Alvarado","Alexis Vega"],
    },
    "Marruecos": {
        "titulares": ["Yassine Bounou","Achraf Hakimi","Romain Saïss","Nayef Aguerd","Yahia Attiyat Allah","Sofyan Amrabat","Azzedine Ounahi","Bilal El Khannouss","Ismael Saibari","Youssef En-Nesyri","Hakim Ziyech"],
        "goleadores": ["Youssef En-Nesyri","Hakim Ziyech","Ismael Saibari","Soufiane Rahimi","Abde Ezzalzouli"],
        "squad": ["Yassine Bounou","Munir Mohamedi","Ahmed Reda Tagnaouti","Achraf Hakimi","Romain Saïss","Nayef Aguerd","Noussair Mazraoui","Yahia Attiyat Allah","Sofyan Amrabat","Azzedine Ounahi","Selim Amallah","Bilal El Khannouss","Hakim Ziyech","Youssef En-Nesyri","Soufiane Rahimi","Abde Ezzalzouli","Ismael Saibari"],
    },
    "Senegal": {
        "titulares": ["Édouard Mendy","Youssouf Sabaly","Kalidou Koulibaly","Abdou Diallo","Fodé Ballo-Touré","Idrissa Gana Gueye","Pape Matar Sarr","Cheikhou Kouyaté","Ismaïla Sarr","Sadio Mané","Boulaye Dia"],
        "goleadores": ["Sadio Mané","Ismaïla Sarr","Boulaye Dia","Nicolas Jackson","Iliman Ndiaye"],
        "squad": ["Édouard Mendy","Alfred Gomis","Sény Dieng","Kalidou Koulibaly","Abdou Diallo","Youssouf Sabaly","Fodé Ballo-Touré","Ismail Jakobs","Idrissa Gana Gueye","Pape Matar Sarr","Nampalys Mendy","Cheikhou Kouyaté","Sadio Mané","Ismaïla Sarr","Boulaye Dia","Nicolas Jackson","Iliman Ndiaye"],
    },
    "Bélgica": {
        "titulares": ["Thibaut Courtois","Timothy Castagne","Jan Vertonghen","Wout Faes","Yannick Carrasco","Amadou Onana","Kevin De Bruyne","Youri Tielemans","Leandro Trossard","Romelu Lukaku","Lois Openda"],
        "goleadores": ["Romelu Lukaku","Lois Openda","Kevin De Bruyne","Leandro Trossard","Johan Bakayoko"],
        "squad": ["Thibaut Courtois","Koen Casteels","Matz Sels","Toby Alderweireld","Jan Vertonghen","Timothy Castagne","Yannick Carrasco","Arthur Theate","Wout Faes","Kevin De Bruyne","Axel Witsel","Youri Tielemans","Amadou Onana","Thomas Meunier","Romelu Lukaku","Lois Openda","Dodi Lukebakio","Leandro Trossard","Johan Bakayoko"],
    },
    "EE.UU.": {
        "titulares": ["Matt Turner","Sergino Dest","Tim Ream","Chris Richards","Antonee Robinson","Tyler Adams","Weston McKennie","Yunus Musah","Christian Pulisic","Folarin Balogun","Giovanni Reyna"],
        "goleadores": ["Folarin Balogun","Christian Pulisic","Giovanni Reyna","Damian Bobadilla","Tim Weah"],
        "squad": ["Matt Turner","Ethan Horvath","Patrick Schulte","Sergino Dest","Tim Ream","Miles Robinson","Joe Scally","Chris Richards","Antonee Robinson","Weston McKennie","Tyler Adams","Yunus Musah","Luca de la Torre","Brenden Aaronson","Christian Pulisic","Folarin Balogun","Giovanni Reyna","Tim Weah","Josh Sargent","Damian Bobadilla"],
    },
    "Japón": {
        "titulares": ["Shuichi Gonda","Hiroki Sakai","Ko Itakura","Shogo Taniguchi","Yuto Nagatomo","Wataru Endo","Hidemasa Morita","Ritsu Doan","Kaoru Mitoma","Daichi Kamada","Keito Nakamura"],
        "goleadores": ["Daichi Kamada","Keito Nakamura","Kaoru Mitoma","Ritsu Doan","Ayase Ueda"],
        "squad": ["Shuichi Gonda","Zion Suzuki","Koki Mori","Hiroki Sakai","Shogo Taniguchi","Ko Itakura","Yuto Nagatomo","Miki Yamane","Wataru Endo","Hidemasa Morita","Sho Ito","Kaoru Mitoma","Ritsu Doan","Daichi Kamada","Keito Nakamura","Ayase Ueda","Junya Ito","Takuma Asano"],
    },
    "Suecia": {
        "titulares": ["Robin Olsen","Emil Krafth","Victor Lindelöf","Niklas Hjalmarsson","Ludwig Augustinsson","Albin Ekdal","Mattias Svanberg","Dejan Kulusevski","Yasin Ayari","Viktor Gyökeres","Alexander Isak"],
        "goleadores": ["Viktor Gyökeres","Alexander Isak","Yasin Ayari","Mattias Svanberg","Dejan Kulusevski"],
        "squad": ["Robin Olsen","Karl-Johan Johnsson","Samuel Brolin","Victor Lindelöf","Niklas Hjalmarsson","Emil Krafth","Ludwig Augustinsson","Carl Starfelt","Albin Ekdal","Mattias Svanberg","Dejan Kulusevski","Yasin Ayari","Sebastian Larsson","Viktor Gyökeres","Alexander Isak","Robin Quaison","Jordan Larsson"],
    },
    "Países Bajos": {
        "titulares": ["Bart Verbruggen","Denzel Dumfries","Virgil van Dijk","Matthijs de Ligt","Nathan Aké","Frenkie de Jong","Tijjani Reijnders","Xavi Simons","Cody Gakpo","Crysencio Summerville","Donyell Malen"],
        "goleadores": ["Cody Gakpo","Crysencio Summerville","Virgil van Dijk","Memphis Depay","Donyell Malen"],
        "squad": ["Bart Verbruggen","Mark Flekken","Remko Pasveer","Virgil van Dijk","Matthijs de Ligt","Stefan de Vrij","Denzel Dumfries","Nathan Aké","Daley Blind","Frenkie de Jong","Tijjani Reijnders","Xavi Simons","Ryan Gravenberch","Teun Koopmeiners","Cody Gakpo","Memphis Depay","Donyell Malen","Crysencio Summerville","Wout Weghorst"],
    },
    "Australia": {
        "titulares": ["Mathew Ryan","Nathaniel Atkinson","Harry Souttar","Miloš Degenek","Aziz Behich","Jackson Irvine","Riley McGree","Aaron Mooy","Nestory Irankunda","Connor Metcalfe","Mathew Leckie"],
        "goleadores": ["Nestory Irankunda","Connor Metcalfe","Mathew Leckie","Craig Goodwin","Mitchell Duke"],
        "squad": ["Mathew Ryan","Danny Vukovic","Joe Gauci","Harry Souttar","Miloš Degenek","Nathaniel Atkinson","Aziz Behich","Joel King","Jackson Irvine","Riley McGree","Aaron Mooy","Cameron Devlin","Nestory Irankunda","Connor Metcalfe","Mathew Leckie","Craig Goodwin","Mitchell Duke"],
    },
    "Corea del Sur": {
        "titulares": ["Kim Seung-gyu","Kim Moon-hwan","Kim Min-jae","Jung Seung-hyun","Kim Jin-su","Hwang In-beom","Jung Woo-young","Lee Kang-in","Heung-min Son","Oh Hyeon-gyu","Hwang Hee-chan"],
        "goleadores": ["Heung-min Son","Oh Hyeon-gyu","Lee Kang-in","Hwang In-beom","Cho Gue-sung"],
        "squad": ["Kim Seung-gyu","Jo Hyeon-woo","Song Bum-keun","Kim Min-jae","Jung Seung-hyun","Kim Jin-su","Kim Moon-hwan","Oh Seok-jun","Lee Kang-in","Hwang In-beom","Paik Seung-ho","Jung Woo-young","Son Jun-ho","Heung-min Son","Oh Hyeon-gyu","Cho Gue-sung","Kwon Chang-hoon","Hwang Hee-chan"],
    },
    # Equipos con squads básicos
    "Argelia":    {"titulares":["Rais M'Bolhi","Ramy Bensebaini","Djamel Benlamri","Aissa Mandi","Hossam Eddine Ouri","Nabil Bentaleb","Youcef Atal","Riyad Mahrez","Sofiane Feghouli","Islam Slimani","Andy Delort"],"goleadores":["Riyad Mahrez","Islam Slimani","Andy Delort","Youcef Atal"],"squad":[]},
    "Austria":    {"titulares":["Patrick Pentz","Stefan Posch","Maximilian Wöber","David Alaba","Philipp Mwene","Nicolas Seiwald","Konrad Laimer","Marcel Sabitzer","Florian Kainz","Christoph Baumgartner","Marko Arnautovic"],"goleadores":["Marcel Sabitzer","Marko Arnautovic","Christoph Baumgartner","Florian Kainz"],"squad":[]},
    "Jordania":   {"titulares":["Yazeed Abulaila","Yazan Al-Naimat","Baha' Faisal","Ahmad Harman","Shadi Shahin","Musa Al-Taamari","Nour Sabaileh","Osama Al-Rashdan","Ali Sulayheen","Ibrahim Salam","Momen Zakaria"],"goleadores":["Baha' Faisal","Yazan Al-Naimat","Musa Al-Taamari"],"squad":[]},
    "Irak":       {"titulares":["Jalal Hassan","Ali Adnan","Safa Hichri","Saad Abdul Amir","Hussein Ali","Amjed Attwan","Bashar Resan","Mohanad Ali","Aymen Hussein","Ahmad Yasin","Ali Jasim"],"goleadores":["Aymen Hussein","Mohanad Ali","Ahmad Yasin"],"squad":[]},
    "Croacia":    {"titulares":["Dominik Livaković","Josip Juranović","Domagoj Vida","Dejan Lovren","Ivan Perišić","Marcelo Brozović","Mateo Kovačić","Luka Modrić","Nikola Vlašić","Ivan Rakitić","Andrej Kramarić"],"goleadores":["Andrej Kramarić","Luka Modrić","Ivan Perišić","Nikola Vlašić"],"squad":[]},
    "Rep. D. del Congo":{"titulares":["Joël Kiassumbua","Chancel Mbemba","Silas Mvumpa","Nathan Ngoy","Yannick Bolasie","Cédric Bakambu","Jonathan David","Théo Bongonda","Tumelo Mafoko","Sébastien Tshimanga","Glody Ngonda"],"goleadores":["Cédric Bakambu","Jonathan David","Yannick Bolasie","Théo Bongonda"],"squad":[]},
    "Uzbekistán": {"titulares":["Timur Suyunov","Sherzod Tursunov","Doniyor Otakhonov","Khusan Murodov","Oybek Bozorov","Otabek Shukurov","Jaloliddin Masharipov","Abbosbek Fayzullaev","Eldor Shomurodov","Jasur Yaxshiboyev","Bobur Abdixoliqov"],"goleadores":["Eldor Shomurodov","Abbosbek Fayzullaev","Jaloliddin Masharipov"],"squad":[]},
    "Irán":       {"titulares":["Alireza Beiranvand","Majid Hosseini","Milad Mohammadi","Sadegh Moharrami","Shojae Khalilzadeh","Saeid Ezatolahi","Ahmad Nourollahi","Ali Karimi","Sardar Azmoun","Mehdi Taremi","Ramin Rezaeian"],"goleadores":["Sardar Azmoun","Mehdi Taremi","Ramin Rezaeian","Mohammad Mohebbi"],"squad":[]},
    "Nueva Zelanda":{"titulares":["Oli Sail","Michael Boxall","Winston Reid","Ryan Thomas","Liberato Cacace","Joe Bell","Callum McCowatt","Matt Garbett","Elijah Just","Chris Wood","Kosta Barbarouses"],"goleadores":["Elijah Just","Chris Wood","Kosta Barbarouses"],"squad":[]},
    "Cabo Verde": {"titulares":["Vozinha","Jair Tavares","Stopira","Zé Luís","Ryan Mendes","Garry Rodrigues","Jamiro Monteiro","Kenny Rocha","Steven Fortes","Willy Semedo","Lisandro Semedo"],"goleadores":["Garry Rodrigues","Ryan Mendes","Jamiro Monteiro","Zé Luís"],"squad":[]},
    "Arabia Saudita":{"titulares":["Mohammed Al-Owais","Sultan Al-Ghanam","Ali Al-Bulayhi","Abdulelah Al-Amri","Hassan Tambakti","Mohamed Kanno","Sami Al-Najei","Salman Al-Faraj","Salem Al-Dawsari","Firas Al-Buraikan","Abdullah Al-Hamdan"],"goleadores":["Salem Al-Dawsari","Firas Al-Buraikan","Abdulelah Al-Amri","Abdullah Al-Hamdan"],"squad":[]},
    "Egipto":     {"titulares":["Mohamed El-Shenawy","Ahmed Hegazi","Omar Kamal","Omar Gaber","Mahmoud Trezeguet","Tarek Hamed","Emam Ashour","Mohamed Salah","Mostafa Mohamed","Marwan Hamdy","Amr El-Sulaya"],"goleadores":["Mohamed Salah","Mostafa Mohamed","Emam Ashour","Trezeguet"],"squad":[]},
    "Ghana":      {"titulares":["Richard Ofori","Andy Yiadom","Alexander Djiku","Daniel Amartey","Baba Rahman","Thomas Partey","Mubarak Wakaso","Kudus Mohammed","Jordan Ayew","André Ayew","Osman Bukari"],"goleadores":["Jordan Ayew","Kudus Mohammed","André Ayew","Osman Bukari"],"squad":[]},
    "Panamá":     {"titulares":["Luis Mejía","Michael Murillo","Fidel Escobar","Harold Cummings","Éric Davis","Adalberto Carrasquilla","José Fajardo","Rolando Blackburn","Ismael Díaz","Édgar Bárcenas","Cecilio Waterman"],"goleadores":["Rolando Blackburn","Ismael Díaz","Cecilio Waterman","Édgar Bárcenas"],"squad":[]},
    "Rep. Checa": {"titulares":["Jiří Staněk","Tomáš Holeš","Ladislav Krejcí","David Jurásek","Jan Bořil","Lukáš Provod","Alex Král","Tomáš Souček","Ondřej Lingr","Patrik Schick","Adam Hložek"],"goleadores":["Patrik Schick","Tomáš Souček","Adam Hložek","Ondřej Lingr"],"squad":[]},
    "Sudáfrica":  {"titulares":["Ronwen Williams","Sifiso Hlanti","Grant Kekana","Rushine De Reuck","Reeve Frosler","Ethan Ngoubane","Teboho Mokoena","Themba Zwane","Percy Tau","Lyle Foster","Bongokuhle Hlongwane"],"goleadores":["Percy Tau","Lyle Foster","Bongokuhle Hlongwane","Themba Zwane"],"squad":[]},
    "Suiza":      {"titulares":["Yann Sommer","Silvan Widmer","Manuel Akanji","Nico Elvedi","Ricardo Rodriguez","Granit Xhaka","Remo Freuler","Ruben Vargas","Djibril Sow","Breel Embolo","Xherdan Shaqiri"],"goleadores":["Breel Embolo","Xherdan Shaqiri","Ruben Vargas","Granit Xhaka"],"squad":[]},
    "Bosnia y Herz.":{"titulares":["Ibrahim Šehić","Anel Ahmedhodžić","Ermin Bičakčić","Sead Kolašinac","Haris Duljevic","Gojko Cimirot","Miralem Pjanić","Edin Visća","Edin Džeko","Hariz Memišević","Jovo Lukić"],"goleadores":["Edin Džeko","Miralem Pjanić","Edin Visća","Hariz Memišević"],"squad":[]},
    "Canadá":     {"titulares":["Maxime Crépeau","Richie Laryea","Kamal Miller","Steven Vitória","Alphonso Davies","Stephen Eustáquio","Atiba Hutchinson","Jonathan Osorio","Tajon Buchanan","Jonathan David","Cyle Larin"],"goleadores":["Jonathan David","Cyle Larin","Alphonso Davies","Tajon Buchanan"],"squad":[]},
    "Qatar":      {"titulares":["Meshaal Barsham","Pedro Miguel","Bassam Al-Rawi","Abdelkarim Hassan","Karim Boudiaf","Homam Ahmed","Ismaël Mohamad","Akram Afif","Almoez Ali","Hassan Al-Haydos","Boualem Khoukhi"],"goleadores":["Akram Afif","Almoez Ali","Boualem Khoukhi","Hassan Al-Haydos"],"squad":[]},
    "Haití":      {"titulares":["Josué Duverger","Andrew Jean-Baptiste","Steeven Saba","Mechack Jérôme","Quentin Poaty","Wilde-Donald Guerrier","James Léandre","Duckens Nazon","Frantzdy Pierrot","Souvernay Pierrot","Schuler Pierre"],"goleadores":["Duckens Nazon","Frantzdy Pierrot","Schuler Pierre"],"squad":[]},
    "Escocia":    {"titulares":["Angus Gunn","Anthony Ralston","Grant Hanley","Kieran Tierney","Andrew Robertson","Callum McGregor","John McGinn","Scott McTominay","Ryan Christie","Che Adams","Lyndon Dykes"],"goleadores":["John McGinn","Che Adams","Scott McTominay","Lyndon Dykes"],"squad":[]},
    "Ecuador":    {"titulares":["Hernán Galíndez","Ángelo Preciado","Félix Torres","Piero Hincapié","Pervis Estupiñán","Moisés Caicedo","Carlos Gruezo","Ángel Mena","Enner Valencia","Gonzalo Plata","Jeremy Sarmiento"],"goleadores":["Enner Valencia","Gonzalo Plata","Moisés Caicedo","Ángelo Preciado"],"squad":[]},
    "Túnez":      {"titulares":["Aymen Dahmen","Ali Abdi","Nader Ghandri","Montassar Talbi","Dylan Bronn","Ellyes Skhiri","Aïssa Laïdouni","Youssef Msakni","Wahbi Khazri","Seifeddine Jaziri","Omar Rekik"],"goleadores":["Wahbi Khazri","Youssef Msakni","Seifeddine Jaziri","Omar Rekik"],"squad":[]},
    "Paraguay":   {"titulares":["Gastón Servio","Gustavo Velázquez","Fabián Balbuena","Omar Alderete","Bruno Valdez","Andrés Cubas","Miguel Almirón","Mathías Villasanti","Ángel Romero","Alejandro Romero","Braian Samudio"],"goleadores":["Miguel Almirón","Ángel Romero","Alejandro Romero","Braian Samudio"],"squad":[]},
    "Turquía":    {"titulares":["Uğurcan Çakır","Zeki Çelik","Merih Demiral","Samet Akaydın","Ferdi Kadıoğlu","Hakan Çalhanoğlu","Orkun Kökçü","Kerem Aktürkoğlu","Arda Güler","Burak Yılmaz","Yusuf Yazıcı"],"goleadores":["Hakan Çalhanoğlu","Arda Güler","Kerem Aktürkoğlu","Burak Yılmaz"],"squad":[]},
    "Costa de Marfil":{"titulares":["Youssouf Diabaté","Serge Aurier","Simon Deli","Odilon Kossounou","Wilfried Zaha","Seko Fofana","Franck Kessié","Ibrahim Sangaré","Simon Adingra","Sébastien Haller","Amad Diallo"],"goleadores":["Amad Diallo","Sébastien Haller","Simon Adingra","Franck Kessié"],"squad":[]},
    "Curazao":    {"titulares":["Eloy Room","Cuco Martina","Vurnon Anita","Rangelo Janga","Leandro Bacuna","Livano Comenencia","Giliano Wijnaldum","Juriën Gaari","Quentin Boel","Elson Hooi","Curaçao Sub"],"goleadores":["Rangelo Janga","Leandro Bacuna","Livano Comenencia"],"squad":[]},
}

# ── Datos base selecciones ────────────────────────────────
SELECCIONES = {
    "Francia":{"rating":92,"ataque":9.2,"defensa":8.8,"estilo":"Contraataque letal, presión alta","fifa_rank":2},
    "Senegal":{"rating":72,"ataque":7.0,"defensa":6.8,"estilo":"Físico, directo, aéreo","fifa_rank":20},
    "Irak":{"rating":48,"ataque":4.5,"defensa":4.2,"estilo":"Defensivo, contraataque","fifa_rank":63},
    "Noruega":{"rating":78,"ataque":8.0,"defensa":7.2,"estilo":"Potencia física, Haaland referencia","fifa_rank":12},
    "Argentina":{"rating":96,"ataque":9.8,"defensa":9.0,"estilo":"Posesión + genialidad de Messi","fifa_rank":1},
    "Argelia":{"rating":65,"ataque":6.2,"defensa":6.0,"estilo":"Organizado, físico","fifa_rank":38},
    "Austria":{"rating":74,"ataque":7.0,"defensa":7.2,"estilo":"Pressing intenso (Rangnick)","fifa_rank":25},
    "Jordania":{"rating":42,"ataque":4.0,"defensa":4.5,"estilo":"Defensivo compacto","fifa_rank":87},
    "Portugal":{"rating":88,"ataque":8.8,"defensa":8.5,"estilo":"Posesión, talento individual","fifa_rank":6},
    "Rep. D. del Congo":{"rating":50,"ataque":4.8,"defensa":5.0,"estilo":"Físico, rápido","fifa_rank":56},
    "Inglaterra":{"rating":87,"ataque":8.5,"defensa":8.3,"estilo":"Potente, directo, balón parado","fifa_rank":5},
    "Croacia":{"rating":75,"ataque":7.2,"defensa":7.5,"estilo":"Posesión, experiencia","fifa_rank":10},
    "Ghana":{"rating":55,"ataque":5.5,"defensa":5.2,"estilo":"Físico, presión intensa","fifa_rank":60},
    "Panamá":{"rating":48,"ataque":4.5,"defensa":5.0,"estilo":"Defensivo compacto","fifa_rank":78},
    "Uzbekistán":{"rating":52,"ataque":5.0,"defensa":5.2,"estilo":"Organizado, técnico","fifa_rank":50},
    "Colombia":{"rating":78,"ataque":7.8,"defensa":7.2,"estilo":"Técnico, creativo por bandas","fifa_rank":13},
    "Rep. Checa":{"rating":66,"ataque":6.2,"defensa":6.5,"estilo":"Organizado, pelota parada","fifa_rank":40},
    "Sudáfrica":{"rating":55,"ataque":5.2,"defensa":5.5,"estilo":"Físico, explosivo en bandas","fifa_rank":58},
    "Suiza":{"rating":76,"ataque":7.0,"defensa":7.8,"estilo":"Sólido, preciso, presión media","fifa_rank":19},
    "Bosnia y Herz.":{"rating":58,"ataque":5.8,"defensa":5.5,"estilo":"Físico, directo","fifa_rank":65},
    "Canadá":{"rating":68,"ataque":6.5,"defensa":6.5,"estilo":"Presión alta, rápido por bandas","fifa_rank":42},
    "Qatar":{"rating":46,"ataque":4.5,"defensa":4.8,"estilo":"Posesión, técnico","fifa_rank":35},
    "Marruecos":{"rating":79,"ataque":7.5,"defensa":8.0,"estilo":"Sólido defensivo, contraataque","fifa_rank":14},
    "Brasil":{"rating":90,"ataque":9.0,"defensa":8.5,"estilo":"Posesión, creatividad, presión","fifa_rank":4},
    "Escocia":{"rating":60,"ataque":5.8,"defensa":6.5,"estilo":"Físico, disciplinado, directo","fifa_rank":45},
    "Haití":{"rating":38,"ataque":3.5,"defensa":3.8,"estilo":"Defensivo, físico","fifa_rank":83},
    "EE.UU.":{"rating":77,"ataque":7.5,"defensa":7.5,"estilo":"Atlético, presión alta, local","fifa_rank":15},
    "Australia":{"rating":62,"ataque":6.0,"defensa":6.5,"estilo":"Físico, rápido en transición","fifa_rank":24},
    "Turquía":{"rating":69,"ataque":7.0,"defensa":6.5,"estilo":"Técnico, ofensivo, inconsistente","fifa_rank":32},
    "Paraguay":{"rating":54,"ataque":5.2,"defensa":5.5,"estilo":"Físico, directo","fifa_rank":48},
    "Alemania":{"rating":87,"ataque":9.0,"defensa":8.2,"estilo":"Presión intensa, muy ofensivo","fifa_rank":16},
    "Curazao":{"rating":38,"ataque":3.5,"defensa":3.5,"estilo":"Primera vez en Mundial","fifa_rank":82},
    "Costa de Marfil":{"rating":72,"ataque":7.2,"defensa":6.8,"estilo":"Rápido, físico, bandas","fifa_rank":30},
    "Ecuador":{"rating":63,"ataque":6.0,"defensa":6.2,"estilo":"Físico, pelota parada","fifa_rank":37},
    "Países Bajos":{"rating":85,"ataque":8.5,"defensa":8.0,"estilo":"Posesión, presión alta, creatividad","fifa_rank":7},
    "Japón":{"rating":74,"ataque":7.5,"defensa":7.0,"estilo":"Rápido, técnico, sorprendente","fifa_rank":18},
    "Suecia":{"rating":70,"ataque":7.0,"defensa":7.0,"estilo":"Físico, directo, organizado","fifa_rank":22},
    "Túnez":{"rating":55,"ataque":5.0,"defensa":5.5,"estilo":"Defensivo, organizado","fifa_rank":28},
    "Bélgica":{"rating":80,"ataque":8.0,"defensa":7.5,"estilo":"Potente, físico, creativo","fifa_rank":3},
    "Egipto":{"rating":65,"ataque":6.5,"defensa":7.0,"estilo":"Organizado, transición","fifa_rank":33},
    "Nueva Zelanda":{"rating":44,"ataque":4.2,"defensa":4.8,"estilo":"Físico, directo","fifa_rank":95},
    "Irán":{"rating":62,"ataque":6.0,"defensa":6.5,"estilo":"Disciplinado, defensivo","fifa_rank":22},
    "España":{"rating":89,"ataque":8.8,"defensa":8.5,"estilo":"Posesión, presión alta, tiki-taka","fifa_rank":8},
    "Cabo Verde":{"rating":52,"ataque":5.0,"defensa":6.5,"estilo":"Muy defensivo, contraataque","fifa_rank":71},
    "Uruguay":{"rating":81,"ataque":8.0,"defensa":8.0,"estilo":"Garra, físico, compacto","fifa_rank":17},
    "Arabia Saudita":{"rating":56,"ataque":5.5,"defensa":5.8,"estilo":"Presión intensa, sorprendente","fifa_rank":54},
    "Corea del Sur":{"rating":68,"ataque":6.5,"defensa":6.8,"estilo":"Físico, rápido, técnico","fifa_rank":23},
    "México":{"rating":72,"ataque":7.2,"defensa":7.0,"estilo":"Rápido, técnico, local","fifa_rank":20},
}

# ── Descarga y procesamiento ──────────────────────────────
def descargar():
    print("  🌐 Descargando datos del Mundial 2026...")
    try:
        r = requests.get(DATA_URL, timeout=15, headers={"User-Agent":"Mozilla/5.0"})
        r.raise_for_status()
        data = r.json()
        print(f"  ✅ Datos actualizados  ({datetime.now().strftime('%d/%m/%Y %H:%M')})\n")
        return data["matches"]
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return []

def separar(partidos):
    j, p = [], []
    for m in partidos:
        (j if "score" in m and m["score"].get("ft") else p).append(m)
    return j, p

def goleadores_torneo(jugados):
    tabla = {}
    for p in jugados:
        for g in p.get("goals1", []):
            n = g["name"]; eq = tr(p["team1"])
            tabla.setdefault(n, {"equipo": eq, "goles": 0, "mins": []})
            tabla[n]["goles"] += 1; tabla[n]["mins"].append(g.get("minute","?"))
        for g in p.get("goals2", []):
            n = g["name"]; eq = tr(p["team2"])
            tabla.setdefault(n, {"equipo": eq, "goles": 0, "mins": []})
            tabla[n]["goles"] += 1; tabla[n]["mins"].append(g.get("minute","?"))
    return sorted(tabla.items(), key=lambda x: x[1]["goles"], reverse=True)

def forma_equipo(equipo_es, jugados):
    res, gf, gc = [], 0, 0
    for p in jugados:
        t1, t2 = tr(p["team1"]), tr(p["team2"])
        s = p["score"]["ft"]
        if t1 == equipo_es:
            gf += s[0]; gc += s[1]
            res.append("W" if s[0]>s[1] else ("D" if s[0]==s[1] else "L"))
        elif t2 == equipo_es:
            gf += s[1]; gc += s[0]
            res.append("W" if s[1]>s[0] else ("D" if s[1]==s[0] else "L"))
    pts = {"W":3,"D":1,"L":0}
    score = sum(pts[r] for r in res) / max(len(res)*3, 1)
    return res, score, gf, gc

def goleadores_reales_equipo(equipo_es, jugados):
    """Devuelve jugadores que han marcado en el torneo para ese equipo."""
    marcadores = {}
    for p in jugados:
        t1, t2 = tr(p["team1"]), tr(p["team2"])
        if t1 == equipo_es:
            for g in p.get("goals1", []):
                marcadores[g["name"]] = marcadores.get(g["name"], 0) + 1
        elif t2 == equipo_es:
            for g in p.get("goals2", []):
                marcadores[g["name"]] = marcadores.get(g["name"], 0) + 1
    return sorted(marcadores.items(), key=lambda x: x[1], reverse=True)

def get_goleadores_prediccion(equipo_es, jugados):
    """Prioriza goleadores reales del torneo, luego squad convocado."""
    reales = goleadores_reales_equipo(equipo_es, jugados)
    sq = SQUADS.get(equipo_es, {})
    
    resultado = []
    # Primero los que ya marcaron
    for nombre, goles in reales:
        resultado.append(f"{nombre} ({goles}⚽ en el torneo)")
    
    # Luego goleadores del squad que no han marcado aún
    for g in sq.get("goleadores", []):
        if g not in [r[0] for r in reales]:
            resultado.append(g)
    
    return resultado[:4]

# ── Motor de predicción ───────────────────────────────────
def predecir(t1, t2, jugados):
    d1 = SELECCIONES.get(t1, {}); d2 = SELECCIONES.get(t2, {})
    if not d1 or not d2: return None
    _, f1, gf1, gc1 = forma_equipo(t1, jugados)
    _, f2, gf2, gc2 = forma_equipo(t2, jugados)

    rat1 = d1["rating"] * 1.06 + f1 * 8
    rat2 = d2["rating"] + f2 * 8
    xg1 = max(0.1, min((d1["ataque"] - d2["defensa"] + 2) * 0.4 * (0.8 + f1 * 0.4) + gf1 * 0.1, 4.5))
    xg2 = max(0.1, min((d2["ataque"] - d1["defensa"] + 2) * 0.4 * (0.8 + f2 * 0.4) + gf2 * 0.1, 4.5))

    diff = (rat1 - rat2) / 15
    pl = 1 / (1 + math.exp(-diff)); pv = 1 - pl
    emp = max(0.13, 0.27 - abs(pl - 0.5) * 0.45)
    pl *= (1 - emp); pv *= (1 - emp)
    tot = pl + pv + emp; pl /= tot; pv /= tot; emp /= tot

    esc = []
    for gl in range(6):
        for gv in range(6):
            p = (xg1**gl * math.exp(-xg1)) / math.factorial(gl) * \
                (xg2**gv * math.exp(-xg2)) / math.factorial(gv) * 100
            if p > 1.5: esc.append({"m": f"{gl}-{gv}", "p": round(p,1)})
    esc.sort(key=lambda x: x["p"], reverse=True)

    res1, _, _, _ = forma_equipo(t1, jugados)
    res2, _, _, _ = forma_equipo(t2, jugados)

    return {"pl":round(pl*100,1),"pe":round(emp*100,1),"pv":round(pv*100,1),
            "xg1":round(xg1,2),"xg2":round(xg2,2),"marc":f"{round(xg1)}-{round(xg2)}",
            "esc":esc[:5],"res1":res1,"res2":res2,"gf1":gf1,"gc1":gc1,"gf2":gf2,"gc2":gc2}

# ── Display ───────────────────────────────────────────────
def sep(c="═"): print("  " + c * 66)
def er(r): return {"W":"✅","D":"🟡","L":"❌"}.get(r,"⬜")
def barra(p, c="█"): return c * int(p // 5)

def mostrar_jugados(jugados):
    sep(); print(f"  📋 RESULTADOS REALES — {len(jugados)} partidos"); sep()
    grupo_act = ""
    for p in jugados:
        g = p.get("group","")
        if g != grupo_act: grupo_act = g; print(f"\n  ── {g} ──")
        t1, t2 = tr(p["team1"]), tr(p["team2"])
        s = p["score"]["ft"]; ht = p["score"].get("ht",["-","-"])
        ico = "🟢" if s[0]>s[1] else ("🟡" if s[0]==s[1] else "🔴")
        print(f"  {ico} {t1:20s} {s[0]}-{s[1]} {t2:20s}  (HT {ht[0]}-{ht[1]})")
        for g in p.get("goals1",[]): print(f"       ⚽ {g['name']} {g.get('minute','')}' — {t1}")
        for g in p.get("goals2",[]): print(f"       ⚽ {g['name']} {g.get('minute','')}' — {t2}")
    print()

def mostrar_goleadores(jugados):
    sep(); print("  🥇 TABLA DE GOLEADORES"); sep()
    tabla = goleadores_torneo(jugados)
    if not tabla: print("  (Sin goles aún)"); return
    for i, (n, d) in enumerate(tabla[:20], 1):
        mins = ", ".join(d["mins"])
        print(f"  {i:2}. {n:28s} {d['goles']}⚽  {d['equipo']:20s}  min: {mins}")
    print()

def mostrar_pred(p, jugados, idx):
    t1, t2 = tr(p["team1"]), tr(p["team2"])
    grupo = p.get("group","?"); fecha = p.get("date","?"); hora = p.get("time","")
    d1 = SELECCIONES.get(t1, {}); d2 = SELECCIONES.get(t2, {})
    sq1 = SQUADS.get(t1, {}); sq2 = SQUADS.get(t2, {})
    pred = predecir(t1, t2, jugados)
    if not pred: print(f"  ⚠️  Sin datos para {t1} o {t2}"); return

    sep(); print(f"  #{idx:02d} | {grupo} | 📅 {fecha}  {hora}"); sep()
    print(f"  🏠 {t1.upper()} (#{d1.get('fifa_rank','?')})  🆚  {t2.upper()} (#{d2.get('fifa_rank','?')})")

    # Titulares
    tit1 = sq1.get("titulares", [])
    tit2 = sq2.get("titulares", [])
    if tit1:
        print(f"\n  👕 XI PROBABLE {t1}:")
        print("     " + " | ".join(tit1[:6]))
        print("     " + " | ".join(tit1[6:]))
    if tit2:
        print(f"\n  👕 XI PROBABLE {t2}:")
        print("     " + " | ".join(tit2[:6]))
        print("     " + " | ".join(tit2[6:]))

    # Forma real
    r1 = " ".join(er(r) for r in pred["res1"]) or "Debut"
    r2 = " ".join(er(r) for r in pred["res2"]) or "Debut"
    print(f"\n  🔥 Forma en el torneo:")
    print(f"     {t1:20s}: {r1}  GF:{pred['gf1']} GC:{pred['gc1']}")
    print(f"     {t2:20s}: {r2}  GF:{pred['gf2']} GC:{pred['gc2']}")

    # Probabilidades
    print(f"\n  📊 PROBABILIDADES:")
    print(f"     🏆 {t1:20s}: {pred['pl']:5.1f}%  {barra(pred['pl'])}")
    print(f"     🤝 Empate             : {pred['pe']:5.1f}%  {barra(pred['pe'])}")
    print(f"     🏆 {t2:20s}: {pred['pv']:5.1f}%  {barra(pred['pv'])}")
    print(f"\n  ⚽ xG: {t1} {pred['xg1']} — {pred['xg2']} {t2}")
    print(f"  🎯 Marcador probable: {pred['marc']}")

    print(f"\n  📈 Escenarios:")
    for e in pred["esc"]: print(f"     {e['m']:5s} → {e['p']:5.1f}%  {barra(e['p'])}")

    # Goleadores usando datos reales + squad
    g1 = get_goleadores_prediccion(t1, jugados)
    g2 = get_goleadores_prediccion(t2, jugados)
    print(f"\n  🌟 Goleadores probables:")
    for g in g1: print(f"     ⚽ {t1}: {g}")
    for g in g2: print(f"     ⚽ {t2}: {g}")

    # Favorito
    fav = t1 if pred["pl"] > pred["pv"] else t2
    df = d1 if fav == t1 else d2
    print(f"\n  🏅 Favorito: {fav}")
    print(f"     🎽 {df.get('estilo','')}")
    print()

def menu(jugados, pendientes):
    while True:
        sep()
        print(f"  🌍 MUNDIAL 2026 | Jugados: {len(jugados)} | Pendientes: {len(pendientes)}")
        sep("─")
        print("  [1] Resultados reales (con goleadores y minutos)")
        print("  [2] Tabla de goleadores del torneo")
        print("  [3] Predecir TODOS los partidos pendientes")
        print("  [4] Predecir UN partido específico")
        print("  [5] Partidos más parejos")
        print("  [6] Ver squad + titulares de un equipo")
        print("  [7] Salir")
        sep("─")
        op = input("  ► Opción: ").strip()

        if op == "1":
            mostrar_jugados(jugados)
        elif op == "2":
            mostrar_goleadores(jugados)
        elif op == "3":
            for i, p in enumerate(pendientes, 1): mostrar_pred(p, jugados, i)
        elif op == "4":
            for i, p in enumerate(pendientes, 1):
                print(f"  {i:3}. [{p.get('group','?')}] {tr(p['team1']):22s} vs {tr(p['team2']):22s}  {p.get('date','')}")
            try:
                n = int(input("\n  ► Número: ")) - 1
                if 0 <= n < len(pendientes): mostrar_pred(pendientes[n], jugados, n+1)
                else: print("  ⚠️  Fuera de rango")
            except ValueError: print("  ⚠️  Número inválido")
        elif op == "5":
            print("\n  📊 Partidos más parejos:\n")
            comp = []
            for p in pendientes:
                t1, t2 = tr(p["team1"]), tr(p["team2"])
                pred = predecir(t1, t2, jugados)
                if pred: comp.append((abs(pred["pl"]-pred["pv"]), p, pred, t1, t2))
            comp.sort(key=lambda x: x[0])
            for _, p, pred, t1, t2 in comp[:10]:
                print(f"  [{p.get('group','?')}] {t1:22s} vs {t2:22s}")
                print(f"       {t1}: {pred['pl']}%  Empate: {pred['pe']}%  {t2}: {pred['pv']}%  | {pred['marc']}\n")
        elif op == "6":
            equipos = sorted(SQUADS.keys())
            for i, e in enumerate(equipos, 1): print(f"  {i:2}. {e}")
            try:
                n = int(input("\n  ► Número: ")) - 1
                eq = equipos[n]
                sq = SQUADS[eq]
                sep(); print(f"  👕 SQUAD — {eq.upper()}"); sep()
                print(f"  Titulares: {', '.join(sq.get('titulares',[]))}")
                print(f"  Goleadores clave: {', '.join(sq.get('goleadores',[]))}")
                reales = goleadores_reales_equipo(eq, jugados)
                if reales:
                    print(f"  Goles en el torneo:")
                    for nombre, goles in reales: print(f"    ⚽ {nombre}: {goles} gol(es)")
                print()
            except: print("  ⚠️  Inválido")
        elif op == "7":
            print("\n  ¡Vamos con toda! 🏆⚽\n"); break
        else:
            print("  ⚠️  Opción no válida")

if __name__ == "__main__":
    sep(); print("  🏆 MUNDIAL 2026 — PREDICTOR EN VIVO"); sep()
    todos = descargar()
    if not todos: print("  ❌ Sin conexión. Verifica internet."); exit(1)
    jugados, pendientes = separar(todos)
    menu(jugados, pendientes)