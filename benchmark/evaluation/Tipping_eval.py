import sys
import os

sys.path.append("../")

from old_benchmark.Tipping_benchmark import benchmark_settings
from logparser.Tipping import LogParser
from evaluation.utils.common import datasets, common_args, unique_output_dir
from evaluation.utils.evaluator_main import evaluator, prepare_results
from evaluation.utils.postprocess import post_average

datasets_2k = [
    "Proxifier",
    "Linux",
    "Apache",
    "Zookeeper",
    "Hadoop",
    "HealthApp",
    "OpenStack",
    "HPC",
    "Mac",
    "OpenSSH",
    "Spark",
    "Thunderbird",
    "BGL",
    "HDFS",
]

datasets_full = [
    "Proxifier",
    "Linux",
    "Apache",
    "Zookeeper",
    "Hadoop",
    "HealthApp",
    "OpenStack",
    "HPC",
    "Mac",
    "OpenSSH",
    "Spark",
    "Thunderbird",
    "BGL",
    "HDFS",
]


if __name__ == "__main__":
    args = common_args()
    data_type = "full" if args.full_data else "2k"
    input_dir = f"../../{data_type}_dataset/"
    output_dir = f"../../result/result_Tipping_{data_type}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    result_file = prepare_results(
        output_dir=output_dir,
        otc=args.oracle_template_correction,
        complex=args.complex,
        frequent=args.frequent,
    )

    if args.full_data:
        datasets = datasets_full
    else:
        datasets = datasets_2k
    for dataset in datasets:
        setting = benchmark_settings[dataset]
        print(setting)
        log_file = setting["log_file"].replace("_2k", f"_{data_type}")
        indir = os.path.join(input_dir, os.path.dirname(log_file))
        if os.path.exists(
            os.path.join(output_dir, f"{dataset}_{data_type}.log_structured.csv")
        ):
            parser = None
            print("parseing result exist.")
        else:
            parser = LogParser
        # run evaluator for a dataset
        evaluator(
            dataset=dataset,
            input_dir=input_dir,
            output_dir=output_dir,
            log_file=log_file,
            LogParser=parser,
            param_dict={
                "log_format": setting["log_format"],
                "indir": indir,
                "outdir": output_dir,
                "symbols": setting["symbols"],
                "special_whites": setting["special_whites"],
                "special_blacks": setting["special_blacks"],
                "tau": setting["tau"],
            },
            otc=args.oracle_template_correction,
            complex=args.complex,
            frequent=args.frequent,
            result_file=result_file,
        )  # it internally saves the results into a summary file

    metric_file = os.path.join(output_dir, result_file)
    post_average(
        metric_file,
        f"Tipping_{data_type}_complex={args.complex}_frequent={args.frequent}",
        args.complex,
        args.frequent,
    )
