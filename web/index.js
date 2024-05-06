const JOBS = ["PLD", "WAR", "DRK", "GNB", "SCH", "SGE", "WHM", "AST", "BLM", "SMN", "RDM", "BLU", "PIC", "BRD", "MCH", "DNC", "DRG", "MNK", "SAM", "NIN", "RPR", "VPR"];
const INTENTS = ["LFG", "LFM", "FC", "OTHER"];
const TAGS = ["C","MC","SHC","HC","WP","W1","Blind","Speed","Farm","Parse","Savage","Ultimate","Extreme","NA","JP","EU","OC","7.0"];
const SELECTOR = "#results"
let _data = {};

function add_jobs_to_filter() {
    let ele = document.querySelector("select[name=jobs]");
    ele.innerHTML = "";

    let opt = document.createElement("option");
    opt.value = "";
    opt.innerText = "(any job)";
    ele.append(opt);

    for (i in JOBS) {
        let opt = document.createElement("option");
        opt.value = JOBS[i];
        opt.innerText = JOBS[i];
        ele.append(opt);
    }

}

function add_intents_to_filter() {
    let ele = document.querySelector("select[name=intent]");
    ele.innerHTML = "";

    for (i in INTENTS) {
        let opt = document.createElement("option");
        opt.value = INTENTS[i];
        opt.innerText = INTENTS[i];
        ele.append(opt);
    }
}

function add_tags_to_filter() {
    let ele = document.querySelector("select[name=tags]");
    ele.innerHTML = "";

    let opt = document.createElement("option");
    opt.value = "";
    opt.innerText = "(any)";
    ele.append(opt);

    for (i in TAGS) {
        let opt = document.createElement("option");
        opt.value = TAGS[i];
        opt.innerText = TAGS[i];
        ele.append(opt);
    }

}

function reset_posts() {
    document.querySelector(SELECTOR).innerHTML = "";
}

function _create_section_name_element(name) {
    let ele = document.createElement("span")
    ele.innerText = name
    return ele
}

function _create_text_info_element(name, value) {
    let ele = document.createElement("div");
    ele.innerHTML = value;
    ele.prepend(_create_section_name_element(name));
    return ele;
}

function display_post(post_data) {

    let rootEle = document.createElement("div");
    rootEle.className = "item";

    let sourceEle = document.createElement("div");
    sourceEle.className = "source";
    sourceEle.innerText = post_data.source;
    rootEle.append(sourceEle);

    rootEle.append(_create_text_info_element("INTENTS:", post_data.tags.join(",")));
    rootEle.append(_create_text_info_element("JOBS:", post_data.roles.join(",")));
    rootEle.append(_create_text_info_element("SUMMARY:", post_data.summary));
    rootEle.append(_create_text_info_element("SCHEDULE:", post_data.schedule));
    rootEle.append(_create_text_info_element("CONTACT:", post_data.contact));
    if (post_data.url) {
        rootEle.append(_create_text_info_element("LINK:", "<a href='" + post_data.url + "' target='_blank'>" + post_data.url + "</a>"));
    }

    document.querySelector(SELECTOR).append(rootEle);
}

function display_posts_filtered() {
    if (!_data) { return; }
    reset_posts();
    let filterJobsEle = document.querySelector("select[name=jobs]");
    let job = filterJobsEle.value;
    let filterIntentEle = document.querySelector("select[name=intent]");
    let intent = filterIntentEle.value;
    let filterTagEle = document.querySelector("select[name=tags]");
    let tag = filterTagEle.value;
    for (i in _data) {
        if (
            _data[i].intent == intent && (!job || _data[i].roles.indexOf(job) >= 0) &&
            (!tag || _data[i].tags.indexOf(tag) >= 0)
        ) {
            display_post(_data[i]);
        }        
    }
}

add_jobs_to_filter();
add_intents_to_filter();
add_tags_to_filter();

fetch("data.json")
    .then(value => value.json())
    .then(data => {
        _data = data;
        display_posts_filtered();
    });

document.querySelector("select[name=jobs]").addEventListener("change", display_posts_filtered);
document.querySelector("select[name=intent]").addEventListener("change", display_posts_filtered);
document.querySelector("select[name=tags]").addEventListener("change", display_posts_filtered);