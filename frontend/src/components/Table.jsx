import { useState } from "react";

function formatDate(isoString) {
  const date = new Date(isoString);

  const day = String(date.getUTCDate()).padStart(2, '0');
  const month = String(date.getUTCMonth() + 1).padStart(2, '0');
  const year = date.getUTCFullYear();
  const hours = String(date.getUTCHours()).padStart(2, '0');
  const minutes = String(date.getUTCMinutes()).padStart(2, '0');

  return `${day}/${month}/${year} ${hours}:${minutes}`;
}


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
            <tr id={job.id}>
              <td className="name-data">{job.name}</td>
              <td>{job.company}</td>
              <td>{formatDate(job.published_date)}</td>
              <td>
                <a href={job.url} target="_blank">Link</a>
              </td>
              <td>{job.website}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
