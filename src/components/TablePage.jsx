import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const TablePage = () => {
	const { category, course } = useParams();
	const [data, setData] = useState([]);
	const [courseMap, setCourseMap] = useState({});
	const [pageTitle, setPageTitle] = useState("Notifications");
	const [hasNotifications, setHasNotifications] = useState(false);

	useEffect(() => {
		fetch(`/api/${category}/${course}`)
			.then((res) => res.json())
			.then((json) => {
				setData(json.data);
				setCourseMap(json.course_map);
				setPageTitle(json.page_title);
				setHasNotifications(json.has_notifications);
				document.title = json.page_title + " - Kerala University";
			})
			.catch((err) => console.error("Error fetching data:", err));
	}, [category, course]);

	return (
		<div>
			<header>
				<div>
					<a href={`/notifications/${course}`}>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
							<path d="M224 0c-17.7 0-32 14.3-32 32l0 19.2C119 66 64 130.6 64 208l0 18.8c0 47-17.3 92.4-48.5 127.6l-7.4 8.3c-8.4 9.4-10.4 22.9-5.3 34.4S19.4 416 32 416l384 0c12.6 0 24-7.4 29.2-18.9s3.1-25-5.3-34.4l-7.4-8.3C401.3 319.2 384 273.9 384 226.8l0-18.8c0-77.4-55-142-128-156.8L256 32c0-17.7-14.3-32-32-32zm45.3 493.3c12-12 18.7-28.3 18.7-45.3l-64 0-64 0c0 17 6.7 33.3 18.7 45.3s28.3 18.7 45.3 18.7s33.3-6.7 45.3-18.7z" />
						</svg>
						{pageTitle === "Notifications" && "Notifications"}
					</a>
					<a href={`/timetables/${course}`}>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
							<path d="M0 96C0 60.7 28.7 32 64 32l384 0c35.3 0 64 28.7 64 64l0 320c0 35.3-28.7 64-64 64L64 480c-35.3 0-64-28.7-64-64L0 96zm64 0l0 64 64 0 0-64L64 96zm384 0L192 96l0 64 256 0 0-64zM64 224l0 64 64 0 0-64-64 0zm384 0l-256 0 0 64 256 0 0-64zM64 352l0 64 64 0 0-64-64 0zm384 0l-256 0 0 64 256 0 0-64z" />
						</svg>
						{pageTitle === "Timetables" && "Timetables"}
					</a>
					<a href={`/results/${course}`}>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512">
							<path d="M320 32c-8.1 0-16.1 1.4-23.7 4.1L15.8 137.4C6.3 140.9 0 149.9 0 160s6.3 19.1 15.8 22.6l57.9 20.9C57.3 229.3 48 259.8 48 291.9l0 28.1c0 28.4-10.8 57.7-22.3 80.8c-6.5 13-13.9 25.8-22.5 37.6C0 442.7-.9 448.3 .9 453.4s6 8.9 11.2 10.2l64 16c4.2 1.1 8.7 .3 12.4-2s6.3-6.1 7.1-10.4c8.6-42.8 4.3-81.2-2.1-108.7C90.3 344.3 86 329.8 80 316.5l0-24.6c0-30.2 10.2-58.7 27.9-81.5c12.9-15.5 29.6-28 49.2-35.7l157-61.7c8.2-3.2 17.5 .8 20.7 9s-.8 17.5-9 20.7l-157 61.7c-12.4 4.9-23.3 12.4-32.2 21.6l159.6 57.6c7.6 2.7 15.6 4.1 23.7 4.1s16.1-1.4 23.7-4.1L624.2 182.6c9.5-3.4 15.8-12.5 15.8-22.6s-6.3-19.1-15.8-22.6L343.7 36.1C336.1 33.4 328.1 32 320 32zM128 408c0 35.3 86 72 192 72s192-36.7 192-72L496.7 262.6 354.5 314c-11.1 4-22.8 6-34.5 6s-23.5-2-34.5-6L143.3 262.6 128 408z" />
						</svg>
						{pageTitle === "Results" && "Results"}
					</a>
				</div>
				<div>
					<select
						className="styled-select"
						value={course}
						id="course-select"
						onChange={(e) => (window.location.href = `/${category}/${e.target.value}`)}
					>
						{Object.entries(courseMap).map(([key, value]) => (
							<option key={key} value={key}>
								{value.title}
							</option>
						))}
					</select>
				</div>
			</header>

			<table>
				<thead>
					<tr>
						<th className="date"></th>
						<th id="semester-heading"></th>
						<th>Description</th>
						<th id="pdf-heading">P</th>
					</tr>
				</thead>
				<tbody>
					{hasNotifications ? (
						data.map((item) =>
							item.notifications?.map((notification, i) => (
								<tr key={notification.description}>
									{i === 0 && <td className="published-date" rowSpan={item.notifications.length}>{item.published_date}</td>}
									<td className="semester-num">{notification.semester_num}</td>
									<td className="description">{notification.description}</td>
									<td className="pdf-link">
										{notification.pdf_link ? (
											<a href={notification.pdf_link} target="_blank" rel="noopener noreferrer">
												<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512">
													<path d="M64 0C28.7 0 0 28.7 0 64L0 448c0 35.3 28.7 64 64 64l256 0c35.3 0 64-28.7 64-64l0-288-128 0c-17.7 0-32-14.3-32-32L224 0 64 0zM256 0l0 128 128 0L256 0zM216 232l0 102.1 31-31c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9l-72 72c-9.4 9.4-24.6 9.4-33.9 0l-72-72c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0l31 31L168 232c0-13.3 10.7-24 24-24s24 10.7 24 24z" />
												</svg>
											</a>
										) : (
											"N/A"
										)}
									</td>
								</tr>
							))
						)
					) : (
						<tr>
							<td colSpan="4" className="no-data">There are no new {pageTitle.toLowerCase()}.</td>
						</tr>
					)}
				</tbody>
			</table>
		</div>
	);
};

export default TablePage;
