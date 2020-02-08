import React from "react";
import { Hero, GetThis } from "sld-component-library";
import Layout from "../components/layout";
import SEO from "../components/seo";
import ExampleList from "../components/ExampleList";

import Places from "../data/Start.json";

export default function Start() {
  return (
    <Layout>
      <SEO title="Home" />
      <div className="is-grey is-orange-bg">
        <Hero places={Places} title="DataWell" />
      </div>
      <div className="is-white-bg">
        <GetThis flag="mango" />
      </div>
      <div className="is-light-grey-bg">
        <div className="row container-small pad-10-t pad-10-b pad-10-l is-grey">
           <h4>Test</h4>
        </div>
        <ExampleList />
      </div>
    </Layout>
  );
}
