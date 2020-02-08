import React from "react";

export default ({ logo }) => (
  <div className="is-white-bg margin-5">
    <div className="row flex padding-0-tb container-small">
      <div className="col-xs-9 flex">
        <img src={logo} className="logo" />
      </div>
    </div>
  </div>
);
