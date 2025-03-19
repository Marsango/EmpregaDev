import { useState } from "react";

export default function Table({ data }) {
  return (
    <div className="table-container">
      <table className="job-table">
        <thead>
          <tr>
            <th>Nome</th>
            <th>Empresa</th>
            <th>Publicado em</th>
            <th>Link</th>
            <th>Website</th>
          </tr>
        </thead>
        <tbody>
          {data.map((job) => (
            <tr>
              <td>{job.title}</td>
              <td>{job.name}</td>
              <td>{job.company}</td>
              <td>{job.published_date}</td>
              <td>
                <a href={job.link}>Link</a>
              </td>
              <td>{job.website}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
