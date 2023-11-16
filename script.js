import { createClient, defaultExchanges } from '@urql/core';
import { getVehicleListQuery, getVehicleDetailsQuery } from './queries.js';
import { renderVehicleList } from './interface';
 
/**
 * For the purpose of this example we use urgl - lightweights GraphQL client.
 * To establish a connection with Chargetrip GraphQL API you need to have an API key.
 * The key in this example is a public one and gives an access only to a part of our extensive database.
 * You need a registered `x-client-id` to access the full database.
 * Read more about an authorisation in our documentation (https://docs.chargetrip.com/#authorisation).
 */
const headers = {
  //Replace this x-client-id and app-id with your own to get access to more vehicles
  'x-client-id': '6533834a9399c506085963ba',
  'x-app-id': '6533834a9399c506085963bc',
};
 
const client = createClient({
  url: 'https://api.chargetrip.io/graphql',
  fetchOptions: {
    method: 'POST',
    headers,
  },
  exchanges: [...defaultExchanges],
});
 
/**
 * You can access a list of all available vehicles using the `vehicleList` query.
 * In this example we use our playground, which has only 12 vehicles available.
 * Chargetrip operates an extensive database of EV makes, editions, and versions,
 * each with their specific consumption models.
 * You need a registered x-client-id to access the full vehicle database.
 * You can obtain a registered x-client-id on https://account.chargetrip.com/
 * **/
export const getVehicleList = () => {
  client
    .query(getVehicleListQuery)
    .toPromise()
    .then(response => {
      renderVehicleList(response.data?.vehicleList);
    })
    .catch(error => console.log(error));
};
 
/**
 * You can access more detailed information of a specific vehicle using the `vehicle` query.
 * This set of data is a limited set of everything that is available.
 * If you need more you can contact us to get access to our `vehiclePremium` query.
 * @param { string } vehicleId - the id of the vehicle that we want the details of
 */
export const getVehicleDetails = (vehicleId, callback) => {
  client
    .query(getVehicleDetailsQuery, { vehicleId })
    .toPromise()
    .then(response => {
      callback(response.data);
    })
    .catch(error => console.log(error));
};




function renderVehicleList(vehicleList) {
    const listElement = document.getElementById('vehicleList');
    vehicleList.forEach(vehicle => {
      const div = document.createElement('div');
      div.textContent = `${vehicle.naming.make} ${vehicle.naming.model}`;
      // Si vous souhaitez ajouter des images
      if(vehicle.media && vehicle.media.image && vehicle.media.image.thumbnail_url) {
        const img = document.createElement('img');
        img.src = vehicle.media.image.thumbnail_url;
        div.appendChild(img);
      }
      listElement.appendChild(div);
    });
  }
  


  // Cette fonction récupère la liste des véhicules
function getVehicleList() {
    const url = 'https://api.chargetrip.io/graphql';
    const headers = {
      'Content-Type': 'application/json',
      'x-client-id': '6533834a9399c506085963ba',
      'x-app-id': '6533834a9399c506085963bc'
    };
    const body = JSON.stringify({
      query: `
        query vehicleList {
          vehicleList(page: 0, size: 20) {
            id
            naming {
              make
              model
              chargetrip_version
            }
            media {
              image {
                thumbnail_url
              }
            }
          }
        }
      `
    });
  
    fetch(url, { method: 'POST', headers: headers, body: body })
      .then(response => response.json())
      .then(data => {
        renderVehicleList(data.data.vehicleList);
      })
      .catch(error => console.error('Error fetching vehicle list:', error));
  }
  
  // Cette fonction récupère les détails d'un véhicule spécifique
  function getVehicleDetails(vehicleId) {
    const url = 'https://api.chargetrip.io/graphql';
    const headers = {
      'Content-Type': 'application/json',
      'x-client-id': '6533834a9399c506085963ba',
      'x-app-id': '6533834a9399c506085963bc'
    };
    const body = JSON.stringify({
      query: `
        query vehicle($vehicleId: ID!) {
          vehicle(id: $vehicleId) {
            naming {
              make
              model
              chargetrip_version
            }
            media {
              image {
                url
              }
              brand {
                thumbnail_url
              }
            }
            // ... ajoutez d'autres champs ici selon vos besoins
          }
        }
      `,
      variables: { vehicleId: vehicleId }
    });
  
    fetch(url, { method: 'POST', headers: headers, body: body })
      .then(response => response.json())
      .then(data => {
        console.log(data.data.vehicle); // Vous pouvez appeler ici une fonction pour traiter les données du véhicule
      })
      .catch(error => console.error('Error fetching vehicle details:', error));
  }
  
  // Enfin, pour déclencher le chargement de la liste des véhicules au chargement de la page :
  document.addEventListener('DOMContentLoaded', getVehicleList);
  