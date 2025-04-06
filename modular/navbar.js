class Header extends HTMLElement {
    constructor() {
      super();
    }
  
    connectedCallback() {
      this.innerHTML = `
        <style>
          nav {
            background-color: #ffffff;  
          }

          @media screen and (min-width: 1024px) {
            .navParent {
              height: auto;
              display: flex;
              align-items: center;
              justify-content: center;
              margin: auto;
            }
  
            .setCenterDiv {
              display: flex;
              align-items: center;
              justify-content: center;
              margin: 20px 0
            }
  
            ul li {
              list-style: none;
              display: inline;
              padding: 0;
            }
  
            a {
              font-weight: 700;
              margin: 0 25px;
              color: #000;
              text-decoration: none;
            }
  
            a:hover {
              padding-bottom: 5px;
              box-shadow: inset 0 -2px 0 0 #0d6efd;
            }
  
            .navImg {
              height: 65px;
              width: 65px;
              margin: 5px 10px 0 0;
            }
  
            .navTitle {
              display: inline-block;
              margin: 0;
              
              font-size: 32px;
              font-weight: 100;
              text-transform: uppercase;
              color: #000000;
            }
  
          }
          
  
          @media screen and (max-width: 1023px) {
            .navParent {
              height: 80px;
            }
  
            ul li {
              list-style: none;
              display: inline;
              padding: 0;
            }
  
            a {
              font-weight: 700;
              margin: 0 25px;
              color: #000;
              text-decoration: none;
            }
  
            a:hover {
              padding-bottom: 5px;
              box-shadow: inset 0 -2px 0 0 #fff;
            }
  
            .navImg {
              height: 65px;
              width: 65px;
              margin: 5px 0 0 8px;
            }
  
            .navTitle {
              display: none;
            }
  
            .setCenterDiv {
              display: none;
            }
          }
        </style>
        <header>
          <nav class="navbar">
            <div class="logo-container">
                <img src="static/trucknew123.png" alt="Truck Logo">
                <div>
                    <div class="company-name">JCTrucking Company</div>
                    <div class="tagline">WE TAKE THE LOAD OFF YOUR BACK</div>
                </div>
            </div>
            <ul class="nav-links">
                <li><a href="#" onclick="showSection('home')" class="active">HOME</a></li>
                <li><a href="#" onclick="showSection('home')">HOME 123</a></li>
                <li><a href="#" onclick="showSection('about')">ABOUT</a></li>
                <li><a href="#" onclick="showSection('trucks-section')">TRUCKS</a></li>
                <li><a href="#" onclick="showSection('services')">SERVICES</a></li>
                <li><a href="#" onclick="showSection('contact')">CONTACT US</a></li>
                <li><a href="{{ url_for('logout') }}">LOGOUT</a></li>
            </ul>
            </nav>
        </header>
      `;
    }
  }
  
  customElements.define('header-component', Header);