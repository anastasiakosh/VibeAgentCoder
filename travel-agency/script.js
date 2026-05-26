document.addEventListener('DOMContentLoaded', () => {                          
     const directionsList = document.getElementById('direction-list');          
                                                                                
     // Sample data for picked directions                                       
     const directions = [                                                       
         "New York City",                                                       
         "Paris",                                                               
         "Tokyo",                                                               
         "London",                                                              
         "Sydney",                                                              
         "Bangkok"                                                              
     ];                                                                         
                                                                                
     directions.forEach(direction => {                                          
         const li = document.createElement('li');                               
         li.textContent = direction;                                            
         directionsList.appendChild(li);                                        
     });                                                                        
 });
