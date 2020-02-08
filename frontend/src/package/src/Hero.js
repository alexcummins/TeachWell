import React, { Fragment } from "react";

export default ({ title, places }) => (
  <div className="row container-small pad-20-t pad-20-b">
    <div className="col-xs-12 col-md-6 pad-10-l">
      <h1 className="is-hero-menu margin-0 is-white">{title}</h1>
      <div className="border" />
      <h4 className="is-hero-sub-text">
        A
        {places.map((item, index) => (
          <Fragment>
            <a
              href={item.url}
              target="_blank"
              className="link-reverse"
              rel="noopener noreferrer"
              key={item.label}
            >
              {`${index === 0 ? ` ` : ``}${item.label}`}
            </a>
            {places.length !== index + 1 ? "/" : " "}
          </Fragment>
        ))}
        boilerplate.
      </h4>
    </div>
  </div>
);
